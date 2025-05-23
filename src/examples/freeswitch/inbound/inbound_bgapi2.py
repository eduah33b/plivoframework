# -*- coding: utf-8 -*-
# Copyright (c) 2011 Plivo Team. See LICENSE for details.

from plivo.core.freeswitch.inboundsocket import InboundEventSocket
from plivo.core.errors import ConnectError
from plivo.utils.logger import StdoutLogger
import gevent.event


class MyEventSocket(InboundEventSocket):
    def __init__(self, host, port, password, filter, log=None):
        InboundEventSocket.__init__(self, host, port, password, filter)
        self.log = log
        self.jobqueue = gevent.event.AsyncResult()

    def on_background_job(self, ev):
        '''
        Recieves callbacks for BACKGROUND_JOB event.
        '''
        self.jobqueue.set(ev)

    def wait_background_job(self):
        '''
        Waits until BACKGROUND_JOB event was caught and returns Event.
        '''
        return self.jobqueue.get()



if __name__ == '__main__':
    log = StdoutLogger()
    try:
        inbound_event_listener = MyEventSocket('127.0.0.1', 8021, 'ClueCon', filter="BACKGROUND_JOB", log=log)
        try:
            inbound_event_listener.connect()
        except ConnectError as e:
            log.error("connect failed: %s" % str(e))
            raise SystemExit('exit')

        fs_bg_api_string = "originate user/1000 &playback(/usr/local/freeswitch/sounds/en/us/callie/base256/8000/liberty.wav)"
        bg_api_response = inbound_event_listener.bgapi(fs_bg_api_string)
        log.info(str(bg_api_response))
        log.info(bg_api_response.get_response())
        if not bg_api_response.is_success():
            log.error("bgapi failed !")
            raise SystemExit('exit')

        job_uuid = bg_api_response.get_job_uuid()
        log.info("bgapi success with Job-UUID " + job_uuid)
        log.info("waiting background job ...")
        ev = inbound_event_listener.wait_background_job()
        log.info("background job: %s" % str(ev))


    except (SystemExit, KeyboardInterrupt): pass

    log.info("exit")
