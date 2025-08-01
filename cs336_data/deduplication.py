import os 

def exact_line_deduplication(input_files, output_directory):

    for path in input_files:
        filename = os.path.basename(path)
        output_path = os.path.join(str(output_directory), filename)

        with open(path, "r", encoding="utf-8") as f:
            seen = set()
            res = []
            for line in f:
                if line not in seen:
                    seen.add(line)
                    res.append(line)
            f.close()

        with open(output_path, "w",  encoding="utf-8") as f:
            f.write("".join(res))

    return
