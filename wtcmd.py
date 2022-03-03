#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Andre Augusto Giannotti Scota (https://sites.google.com/view/a2gs/)

import sys, os, locale
import requests

WTValidAssets = ['BRL-XBT', 'XBT-BRL']

def printUsage(exec: str):
	print('Walltime command line')
	print('-mi\t\tMarket info')
	print('-ob\t\tOrder book')
	print('-lt\t\tLast trades')
	print(f'\t\t\t{exec} -lt [ASSET] [DATE]')
	print('\t\t\t\tASSET = Walltime valid assets')
	print('\t\t\t\tDATE = Last date (YYYY MM DD 24h)')
	print(f'\t\t\tSample: {exec} -lt BRL-XBT \"2022 03 01 16\"')
	print('-aw\t\tAdd withdraw address')
	print('-c\t\tCancel order')
	print('-co\t\tCreate order')
	print('-da\t\tGenerate new deposit address')
	print('-as\t\tGet account statement')
	print('-ai\t\tGet account info')
	print('-go\t\tGet orders')
	print('-id\t\tInform deposit')
	print('-rw\t\tRequest withdraw')

	print(f'\nWalltime valid asstes: {WTValidAssets}')


def getRequest(url: str) -> [bool, int, {}]:
	try:
		urlResponse = requests.get(url)

	except:
		return [False, urlResponse.status_code, {}]

	return [True, urlResponse.status_code, urlResponse.json() if urlResponse.status_code == 200 else {}]


def printMarketInfo() -> bool:
	ret, getRetCode, retJson = getRequest(
		'https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/walltime-info.json')

	if ret == True:
		print(f"Retorno:\n{retJson}")

	return ret


def printLastTrade(asset: str, lasttradedate: str) -> bool:
	ret, getRetCode, retJson = getRequest(
		'https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/meta.json')

	if ret == False:
		return False

	url = 'https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/' + retJson[
		'last_trades_prefix'] + '_' + asset + '_p0.json'

	ret, getRetCode, retJson = getRequest(url)

	if ret == False:
		return False

	print(f'Returno: {retJson}')

def formatReal(value:float) -> "":
	return locale.format_string("%.2f", value, grouping=True, monetary=False)

def printOrderBook():
	ret, getRetCode, retJson = getRequest('https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/meta.json')

	if ret == False:
		return False

	url = 'https://s3.amazonaws.com/data-production-walltime-info/production/dynamic/' + retJson['order_book_prefix'] + '_r' + str(retJson['current_round']) + '_p0.json'

	ret, getRetCode, retJson = getRequest(url)

	if ret == False:
		return False

	print(f'{"COMPRA":^60s}')
	print(f'{"VALOR (R$)":^20s}|{"QTD (BTC)":^20s}|{"TOTAL (R$)":^20s}')
	print(f"{'-' * 20}" + '+' + f"{'-' * 20}" + '+' + f"{'-' * 20}")
	[print(f'{formatReal(eval(i[0])):>20s}|{eval(i[1]):20.8f}|{formatReal(eval(i[0]) / eval(i[1])):>20s}') for i in retJson['brl-xbt']]

	print('\n')

	print(f'{"VENDA":^60s}')
	print(f'{"VALOR (BTC)":^20s}|{"QTD (R$)":^20s}|{"TOTAL (R$)":^20s}')
	print(f"{'-' * 20}" + '+' + f"{'-' * 20}" + '+' + f"{'-' * 20}")
	[print(f'{eval(i[0]):20.8f}|{formatReal(eval(i[1])):>20s}|{formatReal(eval(i[1]) / eval(i[0])):>20s}') for i in retJson['xbt-brl']]

if __name__ == '__main__':
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

	if len(sys.argv) == 2:

		if sys.argv[1] == '-mi':

			if printMarketInfo() == False:
				print('Market Info erro.')

		elif sys.argv[1] == '-ob':

			if printOrderBook() == False:
				print('Order Book erro.')

	elif len(sys.argv) == 4:

		if sys.argv[1] == '-lt':

			if sys.argv[2] in WTValidAssets:

				if printLastTrade(sys.argv[2], sys.argv[3]) == False:
					print("Last Trade erro.")

			else:
				print(f'Asset does not exist: {sys.argv[2]}')

	else:

		if len(sys.argv) != 1:
			print('Parameters erro')

		printUsage(os.path.basename(__file__))