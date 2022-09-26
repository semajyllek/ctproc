


"""

If package used from command line, by calling the following function with the command:

python clinproc --zip_data='/path/to/zip_folder' --write_file='/path/to/write/file.jsonl'

def process_data(
    zip_data, 
    write_file, 
    concat=False, 
    counts=None, 
    max_trials=1e7, 
    start=-1, 
    add_ents=True, 
    mnegs=True, 
    expand=True,
    remove_stops=True,
    id_to_print="", 
    get_only=None
  )

"""

from clinproc.proc import process_data
import argparse

parser = argparse.ArgumentParser(description='cli for clinproc process_data api')
parser.add_argument('--zip_data', help='pathlike to a zipped folder containing XML CT trial data')
parser.add_argument('--write_file', help='pathlike to write location for jsonl file created, one processed trial per line')



parser.add_argument('--concat', action='store_true',
                    help='Boolean, whether to concatenate all fields into a single content field (in addition to other parsed fields), default=False')

parser.add_argument('--max_trials', type=int, default=1e7,
                    help='Integer for max number of files to process, default=1e7')


parser.add_argument('--start_index', type=int, default=-1,
                    help='Integer specifying which index (minus 1) to start at. Useful for debugging or stopped processes, default=-1')


parser.add_argument('--add_ents', action='store_false',
                    help='Boolean, whether to add a field for representing criterias as entities, default=True')


parser.add_argument('--mnegs', action='store_false',
                    help='Boolean, whether to add a field for representing criterias with negative phrases moved to new independent opposite criteria, default=True')


parser.add_argument('--expand', action='store_false',
                    help='Boolean, whether to add a field for representing criterias as expansions of entity-related text values, default=True')



parser.add_argument('--remove_stops', action='store_false',
                    help='Boolean, whether to add a field for representing criterias without stopwords, default=True')


parser.add_argument('--id_to_print', default="",
                    help='String, an ID like NCT81001 supplied by user for printing a single processed clinical trial, debug info. default="')


parser.add_argument('--get_only', default=None, nargs='+', 
                    help="List of strings, user supplied list of NCTID's to process, useful for debugging, default=None")



args = parser.parse_args()



def main():
    process_data(
        zip_data=args.zip_data, 
        write_file=args.write_file, 
        concat=args.concat, 
        max_trials=args.max_trials, 
        start=args.start_index, 
        add_ents=args.add_ents, 
        mnegs=args.mnegs, 
        expand=args.expand,
        remove_stops=args.remove_stops,
        id_to_print=args.id_to_print, 
        get_only=args.get_only
    )

