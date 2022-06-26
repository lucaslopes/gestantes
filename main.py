__author__ = 'https://lucaslopes.me/'

# Imports

from data_load import load_sihsus

# Main

def main():
	
	sihsus, dicio = load_sihsus()
	return sihsus, dicio


__name__ == '__main__' and main()