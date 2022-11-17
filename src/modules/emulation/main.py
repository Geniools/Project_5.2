# Importing fat
from .fat.fat import run_extractor, identify_arch, make_image, infer_network, final_run


def main(path):
    image_id = run_extractor(path)

    if image_id == "":
        result = "Image extraction failed"
    else:
        arch = identify_arch(image_id)
        make_image(arch, image_id)
        infer_network(arch, image_id, None)
        final_run(image_id, arch, None)
        result = "Image extraction successful"

    return result
