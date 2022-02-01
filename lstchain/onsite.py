import os

def create_pro_symlink(output_dir, prod_id):
    pro_dir = f"{output_dir}/../pro"
    if os.path.exists(pro_dir) and os.readlink(pro_dir) is not output_dir:
        os.remove(pro_dir)
        os.symlink(prod_id, pro_dir)

