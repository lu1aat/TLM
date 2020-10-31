import sys
import os
import simplekml

if __name__ == '__main__':
    csv_path = sys.argv[1]
    print("tml-csvkml")
    print(csv_path)

    # Read source file lines
    csv_file = open(csv_path, "r")
    lines = csv_file.readlines()

    # KML
    kml = simplekml.Kml()

    # Points
    path_points = []
    point_id = 0
    one_grid_only = []
    reporters = {}
    for line in lines[1:]:
            fields = line.strip().split(",")
            print(fields)
            if fields[6] in one_grid_only:
                continue
            path_points.append((fields[8], fields[7]))
            day = fields[16].split()[0]
            pnt = kml.newpoint(name=day + " #" +str(point_id), coords=[(fields[8], fields[7])])
            pnt.style.iconstyle.scale = 3  # Icon thrice as big
            # For more icons see http://kml4earth.appspot.com/icons.html#kml-icons
            pnt.style.iconstyle.icon.href = 'http://earth.google.com/images/kml-icons/track-directional/track-none.png'
            point_id = point_id + 1
            one_grid_only.append(fields[6])

            # reporters
            reporters[fields[12]] = (fields[14], fields[13])
            lin_rpt = kml.newlinestring(name=fields[12], description="", coords=[(fields[14], fields[13]), (fields[8], fields[7])])

    # Reporters
    for rpt_call, rpt_data in reporters.items():
        print(rpt_call, rpt_data)
        pnt = kml.newpoint(name=rpt_call, coords=[rpt_data])
        pnt.style.iconstyle.scale = 3  # Icon thrice as big
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/grn-blank.png'

    lin = kml.newlinestring(name="LU1ESY", description="LU1ESY Flight Path", coords=path_points)
    lin.style.linestyle.color = simplekml.Color.red  # Red
    lin.style.linestyle.width = 3

    print(os.path.dirname(csv_path))
    kml_path = os.path.dirname(csv_path) + "/" + os.path.basename(csv_path).split(".")[0] + ".kml"
    print(kml_path)
    kml.save(kml_path)