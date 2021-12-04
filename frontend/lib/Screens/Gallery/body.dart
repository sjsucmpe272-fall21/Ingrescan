import 'package:flutter/material.dart';
import 'package:sliding_up_panel/sliding_up_panel.dart';
import 'package:flutter_auth/Screens/Results/page/result_page_url.dart';

class GalleryPage extends StatefulWidget {
  List<String> imageList;
  List<dynamic> listUserHistory;
  GalleryPage(this.imageList, this.listUserHistory);
  @override
  _GalleryPageState createState() =>
      _GalleryPageState(imageList, listUserHistory);
}

class _GalleryPageState extends State<GalleryPage> {
  final panelController = PanelController();
  final double tabBarHeight = 90;
  List<String> imageList;
  List<dynamic> listUserHistory;
  _GalleryPageState(this.imageList, this.listUserHistory);
  @override
  Widget build(BuildContext context) => Scaffold(
      appBar: AppBar(
        centerTitle: true,
        elevation: 2,
      ),
      body: new GridView.count(
        crossAxisCount: 4,
        childAspectRatio: 1.0,
        padding: const EdgeInsets.all(4.0),
        mainAxisSpacing: 4.0,
        crossAxisSpacing: 4.0,
        children: _getTiles(imageList),
      ));

  List<Widget> _getTiles(List<String> iconList) {
    final List<Widget> tiles = <Widget>[];
    for (int i = 0; i < iconList.length; i++) {
      tiles.add(new Scaffold(
          body: new InkResponse(
        enableFeedback: true,
        child: Container(
          decoration: BoxDecoration(
            image: DecorationImage(
              fit: BoxFit.cover,
              image: NetworkImage(imageList[i]),
            ),
          ),
        ),
        onTap: () => Navigator.push(
          this.context,
          MaterialPageRoute(
            builder: (context) {
              var food = listUserHistory[i]["food"].toString();
              var carbs = listUserHistory[i]["carbohydrates"].toString();
              var calories = listUserHistory[i]["energy"].toString();
              var cholestrol = listUserHistory[i]["cholesterol"].toString();
              var fat = listUserHistory[i]["fat"].toString();
              var fiber = listUserHistory[i]["fiber"].toString();
              var protein = listUserHistory[i]["proteins"].toString();
              var sugar = listUserHistory[i]["sugars"].toString();
              return ResultPageUrl(carbs, calories, cholestrol, fiber, protein,
                  sugar, fat, food, imageList[i]);
            },
          ),
        ),
      )));
    }
    return tiles;
  }
}
