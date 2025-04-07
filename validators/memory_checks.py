import xml.etree.ElementTree as ET

def check_memory_overuse(root, max_memory=1024):
    """
    Checks if any software component exceeds the defined memory limits.
    Default limit: 1024 KB.
    """
    errors = []
    
    for swc in root.findall(".//APPLICATION-SOFTWARE-COMPONENT-TYPE"):
        swc_name = swc.find("SHORT-NAME").text if swc.find("SHORT-NAME") is not None else "Unknown"
        memory_usage = swc.find("MEMORY-USAGE")

        if memory_usage is not None:
            try:
                memory_value = int(memory_usage.text)
                if memory_value > max_memory:
                    errors.append(f"⚠️ Memory overuse detected in {swc_name}: {memory_value} KB (Limit: {max_memory} KB)")
            except ValueError:
                errors.append(f"⚠️ Invalid memory usage value in {swc_name}")
    
    return errors

def validate_mem_map_usage(root):
    """
    Ensures that MEM-MAP sections are correctly defined and used.
    """
    errors = []
    valid_mem_sections = {"ROM", "RAM", "EEPROM"}

    for mem_map in root.findall(".//MEM-MAP"):
        section = mem_map.find("SECTION")
        swc_name = mem_map.find("SWC-NAME").text if mem_map.find("SWC-NAME") is not None else "Unknown"

        if section is None or section.text not in valid_mem_sections:
            errors.append(f"⚠️ Invalid or missing MEM-MAP section in {swc_name}: {section.text if section is not None else 'None'}")
    
    return errors

def check_memory_segment_allocation(root):
    """
    Ensures all memory segments are allocated properly.
    """
    errors = []
    
    defined_segments = set()
    for segment in root.findall(".//MEMORY-SEGMENT"):
        segment_name = segment.find("SHORT-NAME").text if segment.find("SHORT-NAME") is not None else None
        if segment_name:
            defined_segments.add(segment_name)

    for allocation in root.findall(".//MEMORY-ALLOCATION"):
        segment_ref = allocation.find("MEMORY-SEGMENT-REF")
        allocation_name = allocation.find("SHORT-NAME").text if allocation.find("SHORT-NAME") is not None else "Unknown"

        if segment_ref is None or segment_ref.text not in defined_segments:
            errors.append(f"⚠️ Invalid or missing MEMORY-SEGMENT reference for allocation: {allocation_name}")
    
    return errors

# Example Usage
if __name__ == "__main__":
    file_path = "example.arxml"
    
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = []
    errors.extend(check_memory_overuse(root))
    errors.extend(validate_mem_map_usage(root))
    errors.extend(check_memory_segment_allocation(root))

    if errors:
        print("❌ Memory Validation Errors:")
        for error in errors:
            print(error)
    else:
        print("✅ Memory & Resource Management Validation Passed!")
