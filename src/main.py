#!/usr/bin/env python3
"""
Input: POTA activation data
Output: ADIF file for upload to https://pota.app/
"""
import os
import argparse
from gnupass import Secret
import config
import adif
import pota
import logging


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fin", required=True,
                        help="path to input log (.yaml)")
    parser.add_argument("--fout", required=True,
                        help="path to output log (.adi)")
    parser.add_argument("--fdbg", required=True,
                        help="debug intermediate data (.yaml)")
    parser.add_argument("--verbose", action="store_true", default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info(f"APP_VERSION: {config.APP_VERSION}")
    logging.info(f"BUILD_TIME: {config.BUILD_TIME}")

    pota_log = pota.ActivationLog()
    pota_log.read_yaml(args.fin)
    pota_log.augment_with_qrz()
    pota_log.write_yaml(args.fdbg)
    pota_log.write_adi(args.fout)
