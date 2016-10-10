# coding: utf-8
from __future__ import print_function, division

import os

from scripts.batch import batch_parser
from scripts.parser import Area, TYPES


def getopts():
    import argparse
    import textwrap

    """
    Get the command line options.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
        Get geojson with coordinates of area by cadastral number.
        http://pkk5.rosreestr.ru/
        """)
    )
    parser.add_argument('-c', '--code', action='store', type=str, required=False,
                        help='area cadastral number')
    parser.add_argument('-t', '--area_type', action='store', type=int, required=False, default=1,
                        help='area types: %s' % "; ".join(["%s:%s" % (k, v) for k, v in TYPES.items()]))
    parser.add_argument('-p', '--path', action='store', type=str, required=False,
                        help='media path')
    parser.add_argument('-o', '--output', action='store', type=str, required=False,
                        help='output path')
    parser.add_argument('-w', '--wgs', action='store_const', const=True, required=False,
                        help='use WGS84 coordinate system')
    parser.add_argument('-l', '--list', action='store', type=str, required=False,
                        help='path of file with cadastral codes list')
    parser.add_argument('-a', '--attrs', action='store_const', const=True, required=False,
                        help='insert the area attributes in the geojson output')
    # parser.add_argument('-x', '--csv', action='store_const', const=True, required=False,
    #                     help='create CSV table output, use only with --list')
    parser.add_argument('-e', '--epsilon', action='store', type=int, required=False,
                        help='Parameter specifying the approximation accuracy. '
                             'This is the maximum distance between the original curve and its approximation.')
    opts = parser.parse_args()

    return opts


def main():
    # area = Area("38:36:000021:1106")
    # area = Area("38:06:144003:4723")
    # area = Area("38:36:000033:375")
    # area = Area("38:06:143519:6153", area_type=5)

    # code, output, path, epsilon, area_type = "38:06:144003:4723", "", "", 5, 1)

    opt = getopts()
    code = opt.code
    output = opt.output if opt.output else os.path.join("output")
    path = opt.path
    epsilon = opt.epsilon if opt.epsilon else 5
    area_type = opt.area_type if opt.area_type else 1
    json_attrs = opt.attrs if opt.attrs else False
    coord = "EPSG:4326" if opt.wgs else "EPSG:3857"
    # csv = opt.csv

    catalog_path = os.path.join(os.getcwd(), "catalog.json")
    abspath = os.path.abspath(output)

    if opt.list:
        file_name = os.path.splitext(os.path.basename(opt.list))[0]
        f = open(opt.list, 'r')
        codes = f.readlines()

        f.close()
        batch_parser(codes, media_path=path, area_type=area_type, catalog_path=catalog_path, coord_out=coord, output=output,
                     file_name=file_name, with_attrs=json_attrs)

    elif code:
        area = Area(code, media_path=path, area_type=area_type, epsilon=epsilon, with_log=True, catalog=catalog_path,
                    coord_out=coord)
        geojson = area.to_geojson_poly(with_attrs=json_attrs)
        if geojson:
            filename = '%s.geojson' % area.file_name
            geojson_path = os.path.join(abspath, "geojson")
            if not os.path.isdir(geojson_path):
                os.makedirs(geojson_path)
            file_path = os.path.join(geojson_path, filename)
            f = open(file_path, 'w')
            f.write(geojson)
            f.close()
            print(file_path)


if __name__ == "__main__":
    main()