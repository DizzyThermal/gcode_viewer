#!/usr/bin/python3

import argparse
import os
import sys


VIEW_SIMPLE = 0
VIEW_ADVANCED = 1
VIEW_EXPERT = 2

def get_value(value, delimeter=' = ', convert_bool=False):
    str_val = str(value.split(delimeter)[1].strip()).capitalize()
    if str_val == "1" or str_val == "0" and convert_bool:
        return True if str_val == "1" else False

    return str_val


def print_config(config):
    view_str = ''
    if config['view'] == 0:
        view_str = 'Simple'
    elif config['view'] == 1:
        view_str = 'Advanced'
    elif config['view'] == 2:
        view_str = 'Expert'

    print(f"Viewing: {config['gcode_file']} [{view_str}]")
    print()
    print('Layers and perimeters:')
    print()
    print('  Layer height:')
    print(f"    Layer height:                         {config['layer_height']} mm")
    print(f"    First layer height:                   {config['first_layer_height']} mm")
    print()
    print('  Vertical shells:')
    print(f"    Perimeters:                           {config['perimeters']} (minimum)")
    print(f"    Spiral vase:                          {config['spiral_vase']}")
    print()
    print('  Horizontal shells:')
    print(f"    Top Solid layers:                     {config['top_solid_layers']}")
    print(f"    Bottom Solid layers:                  {config['bottom_solid_layers']}")
    print(f"    Top Minimum shell thickness:          {config['top_solid_min_thickness']} mm")
    print(f"    Bottom Minimum shell thickness:       {config['bottom_solid_min_thickness']} mm")
    print()
    if config['view'] > VIEW_SIMPLE:
        print('  Quality (slower slicing) [Advanced+]:')
        if config['view'] > VIEW_ADVANCED:
            print(f"    [E] Extra perimeters if needed:       {config['extra_perimeters']}")
        print(f"    [A] Ensure vertical shell thickness:  {config['ensure_vertical_shell_thickness']}")
        print(f"    [A] Detect thin walls:                {config['thin_walls']}")
        print(f"    [A] Thick bridges:                    {config['thick_bridges']}")
        print(f"    [A] Detect bridging perimeters:       ????")
        print()

    print('  Advanced')
    print(f"    Seam position:                        {config['seam_position']}")
    if config['view'] > VIEW_ADVANCED:
        print(f"    [E] External perimeters first:        {config['external_perimeters_first']}")
    if config['view'] > VIEW_SIMPLE:
        print(f"    [A] Fill gaps:                        {config['gap_fill_enabled']}")
        print(f"    [A] Perimeter generator:              {config['perimeter_generator']}")
    print()
    print('  Fuzzy skin (experimental)')
    print(f"    Fuzzy Skin:                           {config['fuzzy_skin']}")
    if config['view'] > VIEW_SIMPLE:
        print(f"    [A] Fuzzy skin thickness:             {config['fuzzy_skin_thickness']} mm")
        print(f"    [A] Fuzzy skin point distance:        {config['fuzzy_skin_point_dist']} mm")
    print()
    print('Infill:')
    print()
    print('  Infill:')
    print(f"    Fill density:                         {config['fill_density']}")
    print(f"    Fill pattern:                         {config['fill_pattern']}")


def main():
    parser = argparse.ArgumentParser(description='G-Code Settings Viewer')
    parser.add_argument('-f','--file', help='G-Code File', required=True)
    parser.add_argument('-v','--view', help='Slic3r Settings to View: [simple|advanced|expert]', required=False, default='simple')
    args = vars(parser.parse_args())
    config = dict()

    if 'view' in args:
        if args['view'].lower() == 'simple':
            config['view'] = VIEW_SIMPLE
        elif args['view'].lower() == 'advanced':
            config['view'] = VIEW_ADVANCED
        elif args['view'].lower() == 'expert':
            config['view'] = VIEW_EXPERT
        else:
            raise Exception(f"Unknown view value \"{args['view']}\"")

    config['gcode_file'] = args['file']
    if not os.path.exists(config['gcode_file']):
        raise Exception(f"File: \"{config['gcode_file']}\" does not exist, exiting.")
    
    with open(config['gcode_file'], 'r') as gc_file:
        for line in gc_file.readlines():
            # Layer and perimeters
            ## Layer height
            if ' layer_height ' in line:
                config['layer_height'] = get_value(line)
            if ' first_layer_height ' in line:
                config['first_layer_height'] = get_value(line)
            ## Vertical shells
            if ' perimeters ' in line:
                config['perimeters'] = get_value(line)
            if ' spiral_vase ' in line:
                config['spiral_vase'] = get_value(line, convert_bool=True)
            ## Horizontal shells
            if ' top_solid_layers ' in line:
                config['top_solid_layers'] = get_value(line)
            if ' bottom_solid_layers ' in line:
                config['bottom_solid_layers'] = get_value(line)
            if ' top_solid_min_thickness ' in line:
                config['top_solid_min_thickness'] = get_value(line)
            if ' bottom_solid_min_thickness ' in line:
                config['bottom_solid_min_thickness'] = get_value(line)
            ## Quality (slower slicing) [Advanced+]
            if ' extra_perimeters ' in line:
                config['extra_perimeters'] = get_value(line, convert_bool=True)
            if ' ensure_vertical_shell_thickness ' in line:
                config['ensure_vertical_shell_thickness'] = get_value(line, convert_bool=True)
            if ' avoid_crossing_perimeters ' in line:
                config['avoid_crossing_perimeters'] = get_value(line, convert_bool=True)
            if ' avoid_crossing_perimeters_max_detour ' in line:
                config['avoid_crossing_perimeters_max_detour'] = get_value(line)
            if ' thin_walls ' in line:
                config['thin_walls'] = get_value(line, convert_bool=True)
            if ' thick_bridges ' in line:
                config['thick_bridges'] = get_value(line, convert_bool=True)
            ## Advanced
            if ' seam_position ' in line:
                config['seam_position'] = get_value(line)
            if ' external_perimeters_first ' in line:
                config['external_perimeters_first'] = get_value(line, convert_bool=True)
            if ' gap_fill_enabled ' in line:
                config['gap_fill_enabled'] = get_value(line, convert_bool=True)
            if ' perimeter_generator ' in line:
                config['perimeter_generator'] = get_value(line)
            ## Fuzzy skin (experimental)
            if ' fuzzy_skin ' in line:
                config['fuzzy_skin'] = get_value(line)
            if ' fuzzy_skin_thickness ' in line:
                config['fuzzy_skin_thickness'] = get_value(line)
            if 'fuzzy_skin_point_dist ' in line:
                config['fuzzy_skin_point_dist'] = get_value(line)

            # Infill
            if ' fill_density ' in line:
                config['fill_density'] = get_value(line)
            if ' fill_pattern ' in line:
                config['fill_pattern'] = get_value(line)
            if ' support_material ' in line:
                config['support_material'] = get_value(line)
            if ' support_material_auto ' in line:
                config['support_material_auto'] = get_value(line)

        gc_file.close()


    print_config(config)

if __name__ == '__main__':
    main()

