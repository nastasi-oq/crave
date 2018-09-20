#!/usr/bin/env python3
from osgeo import gdal
import csv
import sys, os


def main():
    fname = sys.argv[1]

    gmf_fname = os.path.join("out", "gmf.csv")
    site_fname = os.path.join("out", "site.csv")

    gmf_fp = open(gmf_fname, "w", encoding="utf-8")
    site_fp = open(site_fname, "w", encoding="utf-8")

    gmf_csv = csv.writer(gmf_fp, delimiter=',')
    site_csv = csv.writer(site_fp, delimiter=',')

    gmf_csv.writerow(["rlzi", "sid", "eid", "thick"])
    site_csv.writerow(["site_id", "lon", "lat"])

    raster = gdal.Open(fname)
    print(raster)

    band = raster.GetRasterBand(1)
    print(band)
    rasterArray = raster.ReadAsArray()

    # xsize = raster.RasterXSize
    # ysize = raster.RasterYSize

    x, delta, _, y, _, _ = raster.GetGeoTransform()
    if x > 180.0:
        x = x - 360.0

    rizi = 0
    eid = 0

    sid = 0

    lat_out = y + (delta / 2.0)
    for row in rasterArray:
        lon_out = x + (delta / 2.0)
        for el in row:
            site_csv.writerow([sid, "%.5f" % lon_out, "%.5f" % lat_out])
            gmf_csv.writerow([rizi, sid, eid, el])
            lon_out += delta
            sid += 1
        lat_out += delta


if __name__ == "__main__":
    main()
