# -*- coding: utf-8 -*-
#lint:disable

# proper indentation is for suckers

dummy = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>dummy_path.kmz</name>
	<Style id="s_ylw-pushpin_hl">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ffff0000</color>
			<width>2</width>
		</LineStyle>		
	</Style>
	<StyleMap id="m_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="s_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<LineStyle>
			<color>ffff0000</color>
			<width>2</width>
		</LineStyle>		
	</Style>
{placemarks}
</Document>
</kml>
"""
#lint:enable



placemark = """	<Placemark>
		<name>{name}</name>
		<styleUrl>#m_ylw-pushpin</styleUrl>
		<LineString>
			<tessellate>1</tessellate>
			<coordinates>
				{coords}
			</coordinates>
		</LineString>
	</Placemark>"""


def make_kmz(point_set):
    points = ""
    coord = "{},{},0  "
    for tup in point_set:
        lat, lng = tup[0], tup[1]
        print("adding: <{},{}>".format(lat, lng))
        points += coord.format(lng, lat)
        _placemark = placemark.format(name="1", coords=points)
    with open("points.kmz", 'w') as f:
        f.write(dummy.format(placemarks=_placemark))


pts = [(38.035126, -78.49606400000002, 1.1145630400880656e-12),
(38.03514382694139, -78.49604108410655, 0.0020019998126965836),
(38.0351616622053, -78.49601907299848, 0.004004001225150374),
(38.035179513774395, -78.49599883537614, 0.0060060015989590034),
(38.035197371122635, -78.4959811851786, 0.008006002118401816),
(38.03521527635268, -78.49596678170452, 0.010008002493407338),
(38.03523321682217, -78.49595620878522, 0.01201000334443085),
(38.03525119631127, -78.49594987818425, 0.01401200371779676),
(38.035269235080456, -78.49594803262664, 0.016016004424470362),
(38.03528731576283, -78.4959507438606, 0.018020004654878068),
(38.03530540105918, -78.49595787422328, 0.020020005172598603),
(38.0353235605852, -78.49596915613702, 0.02202400587876621),
(38.03534173578074, -78.49598410093056, 0.0240260062553092),
(38.035359939163385, -78.49600211028216, 0.02602800662801767),
(38.03537816402134, -78.49602245419703, 0.028030007480291667),
(38.03539642099573, -78.49604433170384, 0.03003400770902067),
(38.03541453567929, -78.4960526983257, 0.032036008560013984),
(38.03543236431553, -78.49602996684087, 0.03403800893619102),
(38.03545020379593, -78.49600841474266, 0.03604000930888782),
(38.035468061943035, -78.49598889236664, 0.038042009683430016),]

if __name__ == "__main__":
    make_kmz(pts)
    print(placemark.format(name="myname", coords="mycoords"))