#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gunicorn config."""
import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
