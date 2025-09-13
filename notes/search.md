以下是一些涉及世界地图的开源工程：

# OpenStreetMap：是一个免费、开放的地图数据库，由志愿者社区通过开放协作进行更新和维护。贡献者通过调查、航空照片或卫星图像追踪以及从其他免费许可的地理数据源导入来收集数据。它可用于制作电子地图、提供导航信息、辅助人道主义援助和数据可视化等，数据可导出为其他 GIS 文件格式。

OSM logo
Planet OSM 行星OSM
The files found here are regularly-updated, complete copies of the OpenStreetMap database.
此处的文件是定期更新的完整OpenStreetMap数据库副本。

Files published before 12 September 2012 are distributed under a Creative Commons Attribution-ShareAlike 2.0 license, those published after are Open Data Commons Open Database License 1.0 licensed. For more information, see the project wiki.
2012年9月12日之前发布的文件遵循知识共享署名-相同方式共享2.0许可协议，之后发布的文件则遵循开放数据共享开放数据库1.0许可协议。更多信息，请参见项目维基。

Latest Exports 最新导出
Latest Weekly Planet XML File (torrent) (RSS)
最新每周星球XML文件（种子）（简易信息聚合）

154 GB, created 8 hours ago. 154 GB，创建于8小时前。
md5: eb41d882d45495065872ac53a996957c.
MD5：eb41d882d45495065872ac53a996957c。

Latest Weekly Changesets (torrent) (RSS)
最新每周变更集（种子）（简易信息聚合）

7.3 GB, created 8 hours ago. 7.3 GB，创建于8小时前。
md5: 7b40b8db4b8326e6cc699a43fa482294.
MD5：7b40b8db4b8326e6cc699a43fa482294。

Latest Weekly Planet PBF File (torrent) (RSS)
最新每周行星PBF文件（种子）（简易信息聚合）

83 GB, created 8 hours ago. 83 GB，创建于8小时前。
md5: df6c5dcef8d27ead043fed3b970aee27.
MD5：df6c5dcef8d27ead043fed3b970aee27。

Each week, a new and complete copy of all data in OpenStreetMap is made available as both a compressed XML file and a custom PBF format file. Also available is the 'history' file which contains not only up-to-date data but also older versions of data and deleted data items.
每周，OpenStreetMap 中所有数据的全新完整副本都会以压缩 XML 文件和自定义 PBF 格式文件的形式提供。此外，还有“历史”文件可供使用，该文件不仅包含最新数据，还包括旧版本数据和已删除的数据项。

A smaller file with complete metadata for all changes ('changesets') in XML format is also available.
还提供了一个更小的文件，其中包含所有变更（“变更集”）的完整元数据，格式为XML。
Using the Data 使用数据
You are granted permission to use OpenStreetMap data by the OpenStreetMap License, which also describes your obligations.
您获得了根据《OpenStreetMap 许可协议》使用 OpenStreetMap 数据的权限，该协议也说明了您的义务。

You can process the file or extracts with a variety of tools. Osmosis is a general-purpose command-line tool for converting the data among different formats and databases, and Osm2pgsql is a tool for importing the data into a Postgis database for rendering maps.
你可以使用多种工具来处理文件或提取内容。Osmosis是一款通用的命令行工具，用于在不同格式和数据库之间转换数据，而Osm2pgsql是一款用于将数据导入Postgis数据库以渲染地图的工具。

Processed coastline data derived from OSM data is also needed for rendering usable maps.
从OSM数据衍生而来的已处理海岸线数据对于绘制可用地图也是必需的。

Extracts & Mirrors 提取物和镜像
The complete planet is very large, so you may prefer to use one of several periodic extracts (individual countries or states) from third parties. GeoFabrik.de and BBBike.org are two providers of extracts with up-to-date worldwide coverage.
整个星球的范围非常大，因此您可能更愿意使用第三方提供的几个周期性提取的数据（单个国家或州）。GeoFabrik.de和BBBike.org是两家提供提取数据的机构，其数据覆盖全球且保持最新。

Supporting OSM 支持OSM
OSM data is free to use, but is not free to make or host. The stability and accuracy of OSM.org depends on its volunteers and donations from its users. Please consider making an annual recurring gift to OSM to support the infrastructure, tools, working groups, and other incentives needed to create the map.
OSM数据可以免费使用，但制作和托管并非免费。OSM.org的稳定性和准确性取决于其志愿者以及用户的捐赠。请考虑向OSM进行年度定期捐赠，以支持制作地图所需的基础设施、工具、工作组及其他激励措施。

World Atlas TopoJSON：该项目将 Natural Earth 提供的高质量矢量数据转化为 TopoJSON 格式，包含了不同分辨率（110m, 50m, 和 10m）的世界国家边界和陆地形状数据。支持在浏览器环境下利用 Canvas 或 SVG 渲染地图，也可在 Node.js 环境中结合 node - canvas 来进行服务器端渲染，适用于数据可视化、教育与研究等场景。

Geo Maps：旨在以程序化方式从 OpenStreetMap 等开放数据库中提取高精度的 GeoJSON 地图，提供世界各国的政治边界、海岸线以及地球上的陆地、水域等信息。这些数据均以 GeoJSON 格式提供，还支持将地图转换为其他格式，如 Shapefile、TopoJSON、CSV、SVG 等。

OpenMapTiles：可以将公开可用的 OpenStreetMap 数据转换为可供使用的软件包，其中包含整个地球、各个国家和主要城市的矢量图块。下载的地图图块可以在网站上使用 JavaScript 查看器显示，也可以在 Android 和 iOS 的原生移动应用中使用，甚至可以离线使用，或者转换为传统的栅格图块或高分辨率图像用于打印。

Marble：是 KDE 社区开发的一款开源虚拟地球仪和世界地图集软件，提供了多种地图视图，支持多种在线和离线地图数据源，如 OpenStreetMap、NASA Blue Marble 等。它具有强大的离线功能，用户可以下载地图数据到本地，还支持路线规划与导航、GPS 连接、地理信息搜索、测量距离和面积等功能。

## OpenStreetMap opensource software

以下是针对 C、Go、Python、JavaScript 四种语言的优质开源项目，涵盖地图处理、数据可视化等与地理信息相关的领域，部分基于 OpenStreetMap 数据或类似地图数据：

1. C 语言相关开源项目
   libosmium
   项目地址：https://github.com/osmcode/libosmium
   简介：高效处理 OpenStreetMap 数据的 C++ 库（C 兼容），支持解析 .osm 格式数据、过滤要素（节点、way、关系）、修改地理数据等，适合构建高性能的 OSM 数据处理工具。
   用途：批量处理地图数据、提取特定区域的道路 / 建筑信息、数据格式转换等。
2. Go 语言相关开源项目
   osm
   项目地址：https://github.com/paulmach/osm
   简介：Go 语言的 OpenStreetMap 数据解析库，支持解析 .osm XML/JSON 数据、处理地理要素（节点、路径、关系），并提供地理计算工具（如距离计算、坐标转换）。
   用途：后端服务中集成 OSM 数据解析、构建轻量地图数据处理工具。
   tile38
   项目地址：https://github.com/tidwall/tile38
   简介：基于 Go 的开源地理空间数据库，支持类似 Redis 的 API，可存储和查询地理要素（点、线、多边形），适合实时位置追踪、地理围栏等场景。
   用途：结合地图数据实现位置服务、空间索引查询。
3. Python 语言相关开源项目
   osmnx
   项目地址：https://github.com/gboeing/osmnx
   简介：基于 OpenStreetMap 数据的 Python 库，可快速下载城市道路网、建筑、POI（兴趣点）等数据，并结合 NetworkX 进行网络分析（如最短路径计算）。
   用途：城市交通网络分析、地图可视化、地理数据挖掘。
   folium
   项目地址：https://github.com/python-visualization/folium
   简介：Python 地图可视化库，基于 Leaflet.js，支持在浏览器中渲染交互式地图，可叠加自定义数据（如标记点、热力图）。
   用途：快速生成带地理数据的交互式网页地图，适合数据分析结果展示。
   geopandas
   项目地址：https://github.com/geopandas/geopandas
   简介：扩展 pandas 以支持地理空间数据，可读取 / 写入 GeoJSON、Shapefile 等格式，结合 Matplotlib 或 Plotly 实现地图可视化。
   用途：地理数据清洗、空间分析（如缓冲区计算、叠加分析）。
4. JavaScript 语言相关开源项目
   Leaflet
   项目地址：https://github.com/Leaflet/Leaflet
   简介：轻量级开源交互式地图库，仅 38KB（gzip 后），支持加载 OSM 等地图瓦片、添加标记、绘制图形，适合嵌入网页。
   用途：前端网页地图展示、自定义交互功能（如点击获取坐标、测距）。
   OpenLayers
   项目地址：https://github.com/openlayers/openlayers
   简介：功能强大的开源地图库，支持多种地图数据源（OSM、WMS、GeoJSON 等），适合复杂地图应用（如三维地形、矢量瓦片）。
   用途：企业级地图应用、地理信息系统（GIS）前端。
   MapLibre GL JS
   项目地址：https://github.com/maplibre/maplibre-gl-js
   简介：开源矢量地图渲染库，支持 3D 地图、自定义样式，兼容 Mapbox 风格，可基于 OSM 矢量瓦片构建高性能地图。
   用途：需要 3D 效果或高度自定义样式的地图应用。
   这些项目覆盖了从数据解析、处理到可视化的全流程，可根据具体需求选择（如后端数据处理用 Go/Python 库，前端展示用 JavaScript 库）。

以下是一些基于 OpenStreetMap 数据的完整开源项目：
Organic Maps：是一个适用于 Android 和 iOS 的免费离线地图应用，主要面向旅行者、游客、徒步旅行者和骑自行车的人。它使用众包的 OpenStreetMap 数据，由社区开发，没有广告、跟踪或数据收集。该项目的代码库包含多个部分，如有机地图主项目、iOS 和 Android 的离线地图 API 等。

openrouteservice：这是一款基于 Java 开发的高性能开源路由引擎。它通过整合 OpenStreetMap 的免费地理数据，提供路线规划、等时线分析、矩阵计算、坐标纠偏、数据导出、健康监控等六大核心功能。项目深度定制了 GraphHopper 4.0，支持全球范围的路网分析，且完全开源可扩展，适合搭建物流系统、出行 App 或进行科研分析等。

osr：是一个内存高效的多模式 OpenStreetMap 路由器，旨在实现全球范围的街道路由，支持行人、自行车、汽车等多种模式。该项目通过使用紧凑的数据结构和内存映射文件，使得在经济实惠的低端机器上导入数据成为可能，其数据模型尽可能地直接存储 OpenStreetMap 数据（节点和路径），对于路由目的，只关注作为路径一部分的相关节点。

Geo Maps：这是一个旨在以程序化方式从 OpenStreetMap 等开放数据库中提取高精度 GeoJSON 地图的开源项目。它提供了一种自动化的方法来获取世界各国的政治边界、海岸线以及地球上的陆地、水域等信息，这些数据均以 GeoJSON 格式提供，方便直接在应用中使用。此外，项目还提供了将地图转换为其他格式，如 Shapefile、TopoJSON、CSV、SVG 等的便利工具。

OSMBuildings：是一个开源的 JavaScript 库，用于在 OpenStreetMap 上展示三维建筑物。它是一个轻量级的 WebGL 库，可以将 OpenStreetMap 的数据转换为 3D 建筑模型，提供了简单易用的 API，允许开发者轻松地集成到自己的 Web 应用中，可用于在地图应用中增加 3D 视角、展示城市建筑信息、制作城市规划演示等。

### local deploy no datebase file.

/Volumes/code/mycode/openstreetmap-website

openstreetmap-website-web-1  | /usr/local/bundle/gems/railties-8.0.2.1/lib/rails/application/configuration.rb:463:in `database_configuration': Could not load database configuration. No such file - ["config/database.yml"] (RuntimeError)
