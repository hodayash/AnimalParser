import argparse
import os.path
from animal_parser import parse_url, merge_animals_tables, grab_relevant_data, \
	duplicate_rows, animal_relations, pretty_print, dict_html_cache
from consts import ANIMALS_WIKI_PAGE

def get_args():
	parser = argparse.ArgumentParser(description="Animal Parser lets you parse Wikipedia animal page")
	parser.add_argument("--path", help="path to output file")
	args = parser.parse_args()
	return args


def main(args):
    tables = parse_url(ANIMALS_WIKI_PAGE)
    animals_table = merge_animals_tables(tables)
    relevant_data = grab_relevant_data(animals_table)
    full = duplicate_rows(relevant_data)
    relations = animal_relations(full)
    pretty_print(relations)

    if args.path:
    	try:
    		dict_html_cache(relations, args.path)
    	except os.error:
    		print("[-] error: path does not exist or is not writable")


if __name__ == '__main__':
    main(get_args())