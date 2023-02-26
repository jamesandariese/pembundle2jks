#!/usr/bin/env python3

import argparse
import cryptography
from cryptography.hazmat.primitives.serialization import Encoding
import sys

import jks
import OpenSSL


parser = argparse.ArgumentParser(
                    prog = 'pembundle2jks',
                    description = 'Convert PEM bundles into JKS')
parser.add_argument('files', type=str, nargs='+',
                    help='bundled PEMs to include in output')
parser.add_argument('--storepass', '-P', type=str, nargs='?', default='changeit',
                    help='JKS password (default is fine for a truststore, usually)')
parser.add_argument('--out', '-o', type=str, nargs='?', default='cacerts.jks',
                    help='output JKS file path')

args = parser.parse_args()

pems = []
for fn in args.files:
    with open(fn, 'rb') as f:
        pems.extend(cryptography.x509.load_pem_x509_certificates(f.read()))

ks = jks.KeyStore.new('jks', [jks.TrustedCertEntry.new("%05d"%i, pem.public_bytes(Encoding.DER)) for i, pem in enumerate(pems)])

ks.save(args.out, args.storepass)
