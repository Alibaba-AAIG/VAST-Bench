#!/usr/bin/env bash
_widget_init_environment() {
    export WIDGET_API_LEVEL=7
    export WIDGET_RELEASE_CHANNEL=stable
}
_widget_init_environment
unset -f _widget_init_environment
