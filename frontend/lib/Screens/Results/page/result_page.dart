import 'package:flutter/material.dart';
import 'package:sliding_up_panel/sliding_up_panel.dart';
import 'package:flutter_auth/Screens/Results/widget/main_image_widget.dart';
import 'package:flutter_auth/Screens/Results/widget/tab_widget.dart';
import 'dart:io';
import 'package:flutter_svg/svg.dart';
import 'dart:convert';

class ResultPage extends StatefulWidget {
  final File file;
  final responseData;
  String carbs;
  String calories;
  String cholestrol;
  String fiber;
  String protein;
  String sugar;
  String fat;
  String food;
  List<dynamic> recommended_foods;
  ResultPage(
      this.file,
      this.responseData,
      this.carbs,
      this.calories,
      this.cholestrol,
      this.fiber,
      this.protein,
      this.sugar,
      this.fat,
      this.food,
      this.recommended_foods);
  @override
  _ResultPageState createState() => _ResultPageState(
      file,
      responseData,
      carbs,
      calories,
      cholestrol,
      fiber,
      protein,
      sugar,
      fat,
      food,
      recommended_foods);
}

class _ResultPageState extends State<ResultPage> {
  final panelController = PanelController();
  final double tabBarHeight = 90;
  final responseData;
  String carbs;
  String calories;
  String cholestrol;
  String fiber;
  String protein;
  String sugar;
  String fat;
  String food;
  List<dynamic> recommended_foods;
  final File file;
  _ResultPageState(
      this.file,
      this.responseData,
      this.carbs,
      this.calories,
      this.cholestrol,
      this.fiber,
      this.protein,
      this.sugar,
      this.fat,
      this.food,
      this.recommended_foods);
  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: AppBar(
          backgroundColor: Color.fromRGBO(90, 45, 143, 1),
          title: Text(
            "IngreScan",
            style: TextStyle(color: Colors.white),
          ),
          centerTitle: true,
          elevation: 2,
        ),
        body: SingleChildScrollView(
            child: Column(children: [
          SizedBox(height: 30),
          MainImageWidget(file),
          SizedBox(height: 10),
          Text(food,
              style: TextStyle(
                  color: Colors.grey[800],
                  fontWeight: FontWeight.bold,
                  fontSize: 18)),
          SizedBox(height: 30),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SvgPicture.asset(
                "assets/icons/Carbs.svg",
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Container(
                    alignment: Alignment.center,
                    width: 100.0,
                    child: Text(carbs,
                        style: TextStyle(
                            color: Colors.grey[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 18)))
              ]),
              SizedBox(width: 50),
              SvgPicture.asset(
                "assets/icons/Calories.svg",
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Container(
                    alignment: Alignment.center,
                    width: 100.0,
                    child: Text(calories,
                        style: TextStyle(
                            color: Colors.grey[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 18)))
              ]),
            ],
          ),
          SizedBox(height: 30),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SvgPicture.asset(
                "assets/icons/Cholestrol.svg",
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Container(
                    alignment: Alignment.center,
                    width: 100.0,
                    child: Text(cholestrol,
                        style: TextStyle(
                            color: Colors.grey[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 18)))
              ]),
              SizedBox(width: 50),
              SvgPicture.asset(
                "assets/icons/Fibre.svg",
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Container(
                    alignment: Alignment.center,
                    width: 100.0,
                    child: Text(fiber,
                        style: TextStyle(
                            color: Colors.grey[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 18)))
              ]),
            ],
          ),
          SizedBox(height: 30),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SvgPicture.asset(
                "assets/icons/Protein.svg",
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Container(
                    alignment: Alignment.center,
                    width: 100.0,
                    child: Text(protein,
                        style: TextStyle(
                            color: Colors.grey[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 18)))
              ]),
              SizedBox(width: 50),
              SvgPicture.asset(
                "assets/icons/Sugar.svg",
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Container(
                    alignment: Alignment.center,
                    width: 100.0,
                    child: Text(sugar,
                        style: TextStyle(
                            color: Colors.grey[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 18)))
              ]),
            ],
          ),
          SizedBox(height: 30),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              SvgPicture.asset(
                "assets/icons/Fat.svg",
                height: MediaQuery.of(context).size.height * 0.05,
              ),
              Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                Container(
                    alignment: Alignment.center,
                    width: 100.0,
                    child: Text(fat,
                        style: TextStyle(
                            color: Colors.grey[800],
                            fontWeight: FontWeight.bold,
                            fontSize: 18)))
              ]),
            ],
          ),
          SizedBox(height: 30),
          Text(recommended_foods.toString(),
              style: TextStyle(
                  color: Colors.grey[800],
                  fontWeight: FontWeight.bold,
                  fontSize: 18))
        ])),
      );

  Widget buildSlidingPanel({
    @required PanelController panelController,
    @required ScrollController scrollController,
    @required String responseData,
  }) =>
      DefaultTabController(
        length: 1,
        child: Scaffold(
          appBar: buildTabBar(
            onClicked: panelController.open,
          ),
          body: TabBarView(
            children: [
              TabWidget(
                  scrollController: scrollController,
                  responseData: responseData),
            ],
          ),
        ),
      );

  Widget buildTabBar({
    @required VoidCallback onClicked,
  }) =>
      PreferredSize(
        preferredSize: Size.fromHeight(tabBarHeight - 8),
        child: GestureDetector(
          onTap: onClicked,
          child: AppBar(
              title: buildDragIcon(), // Icon(Icons.drag_handle),
              centerTitle: true,
              bottom: TabBar(
                tabs: [
                  Tab(child: Text('')),
                ],
              ),
              automaticallyImplyLeading: false),
        ),
      );

  Widget buildDragIcon() => Container(
        decoration: BoxDecoration(
          color: Colors.black.withOpacity(0.3),
          borderRadius: BorderRadius.circular(8),
        ),
        width: 40,
        height: 8,
      );
}
