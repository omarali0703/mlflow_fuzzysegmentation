import io
from os import write, path
import xml.etree.ElementTree as ET

# Retrieve the segmentations from the RST file.
# if Bin, return the FuzzySeg version (binary), otherwise return a parsed list
# Output_location is not including the file name itself. This is taken from the location.
# The location variable includes the file name we are parsing. I do not 
def parse_rs3(location, output_location=None, bin=True):
    rst = ET.parse(location)
    root = rst.getroot()
    segments = []
    for child in root:
        child_tag = child.tag
        child_attr = child.attrib
        # Enforce str type.
        if bin:
            segments = '1'
        if child_tag == 'body':
            # parse the segments in this section
            for segment_tag in child:
                segement_text = segment_tag.text
                if not bin:
                    segments.append(segement_text)
                else:
                    if segement_text:
                        segments += '0'*len(segement_text.split(' '))
                        segments += '1'

        elif child_tag == 'head':
            # TODO Parse the RST structure here?
            # TODO RST Main structure is stored here. Links and deps are determined here.
            pass
    if output_location:
        output_location = open(output_location, 'w')
        file_name = len(location.split('/'))


    return segments

# Write_to_file is the location of the folder.
# This should not include the filename at the end. 
# This is generated using the location var.
def get_original_text(location=None, write_to_file=None):
    rst = ET.parse(location)
    root = rst.getroot()
    filename = location.split('/')
    filename = filename[len(filename)-1]
    filename = filename.split('.')[0]

    original_text = ''
    for child in root:
        child_tag = child.tag
        child_attr = child.attrib
        if child_tag == 'body':
            # parse the segments in this section
            for segment_tag in child:
                segement_text = segment_tag.text
                if segement_text != None:
                    original_text += segement_text

    if write_to_file:
        write_to_file = os.path.join(write_to_file, filename)
        output_file = open(write_to_file, 'w')
        output_file.write(original_text)
        output_file.close()
        return write_to_file # Return the location
    return original_text

# test_text = get_original_text('../dependencies/phd_datasets/gum_dataset/rst/rstweb/GUM_academic_mutation.rs3')
test_text = parse_rs3('../dependencies/phd_datasets/gum_dataset/rst/rstweb/GUM_academic_mutation.rs3')
print(test_text)

def get_deps(location=None, rst_data=None):
    if location and not rst_data:
        pass
    elif rst_data and not location:
        pass