#!/bin/bash

SUPERVISOR_PATH=/usr/local/bin/supervisorctl
$SUPERVISOR_PATH stop screen_callback:screen_callback-13000
$SUPERVISOR_PATH stop screen_callback:screen_callback-13001
$SUPERVISOR_PATH stop screen_callback:screen_callback-13002
$SUPERVISOR_PATH stop screen_callback:screen_callback-13003
$SUPERVISOR_PATH stop screen_other
$SUPERVISOR_PATH stop screen_play
$SUPERVISOR_PATH stop screen_static

$SUPERVISOR_PATH start screen_callback:screen_callback-13000
$SUPERVISOR_PATH start screen_callback:screen_callback-13001
$SUPERVISOR_PATH start screen_callback:screen_callback-13002
$SUPERVISOR_PATH start screen_callback:screen_callback-13003
$SUPERVISOR_PATH start screen_other
$SUPERVISOR_PATH start screen_play
$SUPERVISOR_PATH start screen_static
