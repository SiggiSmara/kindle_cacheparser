import sys
import os
import csv
from pathlib import Path
import typer
import xmltodict

def input_sanity_check(in_file:Path, out_file:Path):
    if not in_file.is_file():
        sys.exit(f"Cant' find input kindle {in_file}")
    else:
        print(f"kindle cache file: {in_file}")

    print(f"output file: {out_file}")
    if not out_file.parent.absolute().is_dir():
        print(f"output_file.parent.absolute as folde not found.. creating it...")
        os.makedirs(out_file.parent.absolute(), exist_ok=True)

def normalize_name(last_first:str):
    return " ".join(last_first.split(", ")[::-1])

def get_list(in_file:Path):
    with open(in_file, "r") as fp:
        my_dict = xmltodict.parse(fp.read())
    try:
        my_dict = my_dict["response"]["add_update_list"]["meta_data"]
    except IndexError:
        sys.exit("No meta data found in xml file")
    for one_meta in my_dict:
        # simplify the structure for title:
        one_meta["title"] = one_meta["title"]["#text"]
        #simplify the structure for authors:
        if "authors" in one_meta:
            if "author" in one_meta["authors"]:
                if isinstance(one_meta["authors"]["author"], dict):
                    one_meta["authors"] = [normalize_name(one_auth["#text"]) for key,one_auth in one_meta["authors"].items()]
                else:
                    one_meta["authors"] = [normalize_name(one_auth["#text"]) for one_auth in one_meta["authors"]["author"]]
                # if len(one_meta["authors"]) > 1:
                #     print(", ".join(one_meta["authors"]))
                if len(one_meta["authors"]) > 0:
                    one_meta["author"] = one_meta["authors"][0]
                one_meta["authors"] = ", ".join(one_meta["authors"])

        #simplify the structure for publishers:
        if one_meta["publishers"] is not None:
            if isinstance(one_meta["publishers"]["publisher"], str):
                one_meta["publishers"] = [one_meta["publishers"]["publisher"],]
            else:
                one_meta["publishers"] = [one_auth for one_auth in one_meta["publishers"]["publisher"]]
            if len(one_meta["publishers"]) > 0:
                one_meta["publisher"] = one_meta["publishers"][0]
            one_meta["publishers"] = ",".join(one_meta["publishers"])
            # if len(one_meta["publishers"]) > 1:
            #     print(one_meta["publishers"])
    return my_dict

def write_csv(kindle_list:list, out_file:Path):
    csv_headers = {
        "ASIN":"ASIN",
        "title":"title",
        "authors":"authors",
        "author":"author",
        "publishers":"publishers",
        "publisher":"publisher",
        "publication_date":"publication date",
        "purchase_date":"purchase date",
        "textbook_type":"textbook type",
        "cde_contenttype":"cde contenttype",
        "content_type":"content type",
        "date_read":"date read",
        "date_added":"date added"
    }
    with open(out_file, "w") as fp:
        my_writer = csv.DictWriter(
            fp, 
            fieldnames=csv_headers.values(), 
            dialect="excel", 
            quoting=csv.QUOTE_ALL
        )
        my_writer.writeheader()
        for one_row in kindle_list:
            try:
                my_row = {key.replace("_"," "):item for key,item in one_row.items() if key in csv_headers }
                my_row["date read"] = my_row["purchase date"]
                my_row["date added"] = my_row["purchase date"]
                
                my_writer.writerow(my_row)
                # my_writer.writerow(one_row)
            except ValueError as e:
                print(e)
                print(my_row.keys())
                # print(one_row.keys())

def main(in_file:Path, out_file:Path = None):
    if out_file is None:
        out_file = Path(".") / "kindle_cachefile.csv"
    input_sanity_check(in_file=in_file, out_file=out_file)
    my_list = get_list(in_file=in_file)
    print(len(my_list))
    write_csv(kindle_list=my_list, out_file=out_file)
    
if __name__ == '__main__':
    typer.run(main)