#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Solver module. """

import asyncio
import json
import sys
import time
import traceback

from pyppeteer.util import merge_dict
from user_agent import generate_navigator_js

from nonocaptcha.base import Base
from nonocaptcha.audio import SolveAudio
from nonocaptcha.image import SolveImage
from nonocaptcha.launcher import Launcher
from nonocaptcha import util
from nonocaptcha.exceptions import (SafePassage, ButtonError, DefaceError,
                                    PageError, nonocaptchaError)


class Solver(Base):
    browser = None
    launcher = None
    proc_count = 0
    proc = None

    def __init__(
        self,
        pageurl,
        sitekey,
        loop=None,
        proxy=None,
        proxy_auth=None,
        options={},
        **kwargs,
    ):
        self.options = merge_dict(options, kwargs)
        self.url = pageurl
        self.sitekey = sitekey
        self.loop = loop or asyncio.get_event_loop()
        self.proxy = f"http://{proxy}" if proxy else proxy
        self.proxy_auth = proxy_auth
        self.proc_id = self.proc_count
        type(self).proc_count += 1

    async def start(self):
        """Begin solving"""
        start = time.time()
        try:
            self.browser = await self.get_new_browser()
            self.page = await self.browser.newPage()
            if self.should_block_images:
                await self.page.setRequestInterception(True)
                self.block_images()
            if self.proxy_auth:
                await self.page.authenticate(self.proxy_auth)
            self.log(f"Starting solver with proxy {self.proxy}")
            await self.set_bypass_csp()
            await self.goto()
            await self.deface()
            result = await self.solve()
        except nonocaptchaError as e:
            self.log(f"{e} {type(e)}")
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e
        finally:
            try:
                if isinstance(result, dict):
                    status = result['status'].capitalize()
                    self.log(f"Result: {status}")
            except NameError:
                result = None
            end = time.time()
            elapsed = end - start
            await self.cleanup()
            self.log(f"Time elapsed: {elapsed}")
            return result

    def block_images(self):
        async def handle_request(request):
            if (request.resourceType == 'image'):
                await request.abort()
            else:
                await request.continue_()

        self.page.on('request', handle_request)

    async def cleanup(self):
        if self.browser:
            await self.browser.close()
            self.log('Browser closed')

    async def set_bypass_csp(self):
        await self.page._client.send(
            "Page.setBypassCSP", {'enabled': True})

    async def get_new_browser(self):
        """Get a new browser, set proxy and arguments"""
        args = [
            '--cryptauth-http-host ""',
            '--disable-accelerated-2d-canvas',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-browser-side-navigation',
            '--disable-client-side-phishing-detection',
            '--disable-default-apps',
            '--disable-dev-shm-usage',
            '--disable-device-discovery-notifications',
            '--disable-extensions',
            '--disable-features=site-per-process',
            '--disable-hang-monitor',
            '--disable-java',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--disable-setuid-sandbox',
            '--disable-sync',
            '--disable-translate',
            '--disable-web-security',
            '--disable-webgl',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--no-sandbox',
            # Automation arguments
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain']
        if self.proxy:
            args.append(f"--proxy-server={self.proxy}")
        if "args" in self.options:
            args.extend(self.options.pop("args"))
        self.options.update({
            "headless": self.headless,
            "args": args,
            #  Silence Pyppeteer logs
            "logLevel": "CRITICAL"})
        self.launcher = Launcher(self.options)
        browser = await self.launcher.launch()
        return browser

    async def cloak_navigator(self):
        """Emulate another browser's navigator properties and set webdriver
           false, inject jQuery.
        """
        jquery_js = await util.load_file(self.jquery_data)
        override_js = await util.load_file(self.override_data)
        navigator_config = generate_navigator_js(
            os=("linux", "mac", "win"), navigator=("chrome"))
        navigator_config["mediaDevices"] = False
        navigator_config["webkitGetUserMedia"] = False
        navigator_config["mozGetUserMedia"] = False
        navigator_config["getUserMedia"] = False
        navigator_config["webkitRTCPeerConnection"] = False
        navigator_config["webdriver"] = False
        dump = json.dumps(navigator_config)
        _navigator = f"const _navigator = {dump};"
        await self.page.evaluateOnNewDocument(
            "() => {\n%s\n%s\n%s}" % (_navigator, jquery_js, override_js))
        return navigator_config["userAgent"]

    async def wait_for_deface(self):
        """Overwrite current page with reCAPTCHA widget and wait for image
           iframe to appear on dom before continuing.

           Function x is an odd hack for multiline text, but it works.
        """
        html_code = await util.load_file(self.deface_data)
        deface_js = (
            (
                """() => {
    var x = (function () {/*
        %s
    */}).toString().match(/[^]*\/\*([^]*)\*\/\}$/)[1];
    document.open();
    document.write(x)
    document.close();
}
"""
                % html_code)
            % self.sitekey)
        await self.page.evaluate(deface_js)
        func = """() => {
    frame = $("iframe[src*='api2/bframe']")
    $(frame).load( function() {
        window.ready_eddy = true;
    });
    if(window.ready_eddy){
        return true;
    }else{
        // I don't think this is necessary but it won't hurt...
        var evt = document.createEvent('Event');
        evt.initEvent('load', false, false);
        window.dispatchEvent(evt);
    }
}"""
        await self.page.waitForFunction(func, timeout=self.deface_timeout)

    async def goto(self):
        """Navigate to address"""
        user_agent = await self.cloak_navigator()
        await self.page.setUserAgent(user_agent)
        try:
            await self.loop.create_task(
                self.page.goto(
                    self.url,
                    timeout=self.page_load_timeout,
                    waitUntil="domcontentloaded",))
        except asyncio.TimeoutError:
            raise PageError("Page loading timed-out")
        except Exception as exc:
            raise PageError(f"Page raised an error: `{exc}`")

    async def deface(self):
        try:
            await self.loop.create_task(self.wait_for_deface())
        except asyncio.TimeoutError:
            raise DefaceError("Problem defacing page")

    async def solve(self):
        """Click checkbox, otherwise attempt to decipher audio"""
        await self.get_frames()
        await self.loop.create_task(self.wait_for_checkbox())
        await self.click_checkbox()
        try:
            result = await self.loop.create_task(
                self.check_detection(self.animation_timeout))
        except SafePassage:
            return await self._solve()
        else:
            if result["status"] == "success":
                code = await self.g_recaptcha_response()
                if code:
                    result["code"] = code
                    return result
            else:
                return result

    async def _solve(self):
        # Coming soon...
        solve_image = False
        if solve_image:
            self.image = SolveImage(
                self.page,
                self.proxy,
                self.proxy_auth,
                self.proc_id)
            solve = self.image.solve_by_image
        else:
            self.audio = SolveAudio(
                self.page,
                self.loop,
                self.proxy,
                self.proxy_auth,
                self.proc_id)
            await self.loop.create_task(self.wait_for_audio_button())
            result = await self.click_audio_button()
            if isinstance(result, dict):
                if result["status"] == "detected":
                    return result
            solve = self.audio.solve_by_audio

        result = await self.loop.create_task(solve())
        if result["status"] == "success":
            code = await self.g_recaptcha_response()
            if code:
                result["code"] = code
                return result
        else:
            return result

    async def wait_for_checkbox(self):
        """Wait for checkbox to appear."""
        try:
            await self.checkbox_frame.waitForFunction(
                "$('#recaptcha-anchor').length",
                timeout=self.animation_timeout)
        except ButtonError:
            raise ButtonError("Checkbox missing, aborting")

    async def click_checkbox(self):
        """Click checkbox on page load."""
        if self.keyboard_traverse:
            self.body = await self.page.J("body")
            await self.body.press("Tab")
            await self.body.press("Enter")
        else:
            self.log("Clicking checkbox")
            checkbox = await self.checkbox_frame.J("#recaptcha-anchor")
            await self.click_button(checkbox)

    async def wait_for_audio_button(self):
        """Wait for audio button to appear."""
        try:
            await self.image_frame.waitForFunction(
                "$('#recaptcha-audio-button').length",
                timeout=self.animation_timeout)
        except ButtonError:
            raise ButtonError("Audio button missing, aborting")

    async def click_audio_button(self):
        """Click audio button after it appears."""
        if self.keyboard_traverse:
            await self.body.press("Enter")
        else:
            self.log("Clicking audio button")
            audio_button = await self.image_frame.J("#recaptcha-audio-button")
            await self.click_button(audio_button)
        try:
            result = await self.check_detection(self.animation_timeout)
        except SafePassage:
            pass
        else:
            return result

    async def g_recaptcha_response(self):
        code = await self.page.evaluate("$('#g-recaptcha-response').val()")
        return code
