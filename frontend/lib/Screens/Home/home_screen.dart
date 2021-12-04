import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:flutter_auth/Screens/Results/page/result_page.dart';
import 'package:flutter_auth/Screens/Gallery/body.dart';
import 'package:path/path.dart';
import 'package:async/async.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'dart:convert';
import 'package:flutter/foundation.dart';

class LifecycleEventHandler extends WidgetsBindingObserver {
  final AsyncCallback resumeCallBack;
  final AsyncCallback suspendingCallBack;

  LifecycleEventHandler({
    this.resumeCallBack,
    this.suspendingCallBack,
  });

  @override
  Future<void> didChangeAppLifecycleState(AppLifecycleState state) async {
    switch (state) {
      case AppLifecycleState.resumed:
        if (resumeCallBack != null) {
          await resumeCallBack();
        }
        break;
      case AppLifecycleState.inactive:
      case AppLifecycleState.paused:
      case AppLifecycleState.detached:
        if (suspendingCallBack != null) {
          await suspendingCallBack();
        }
        break;
    }
  }
}

class CameraPage extends StatefulWidget {
  String id;
  CameraPage(this.id);
  @override
  _CameraPageState createState() => _CameraPageState(id);
}

class _CameraPageState extends State<CameraPage> {
  String id;
  _CameraPageState(this.id);
  List<CameraDescription> _cameras;
  CameraController _controller;
  bool _isReady = false;
  PermissionStatus _status;
  String carbs;
  String calories;
  String cholestrol;
  String fiber;
  String protein;
  String sugar;
  String fat;
  String food;
  List<dynamic> recommended_foods;
  var responseData;
  @override
  void initState() {
    super.initState();
    PermissionHandler()
        .checkPermissionStatus(PermissionGroup.camera)
        .then(_updateStatus);
    WidgetsBinding.instance.addObserver(LifecycleEventHandler(
        resumeCallBack: () async => setState(() {
              // do something
            })));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Color.fromRGBO(90, 45, 143, 1),
          title: Text(
            "IngreScan",
            style: TextStyle(color: Colors.white),
          ),
          centerTitle: true,
          elevation: 2,
        ),
        backgroundColor: Colors.white,
        floatingActionButton: getFooter());
  }

  Widget getFooter() {
    return Padding(
      padding: const EdgeInsets.only(left: 30, top: 60),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              InkWell(
                child: CircleAvatar(
                  backgroundColor: Colors.white,
                  backgroundImage: AssetImage("assets/icons/history.png"),
                  radius: 60,
                ),
                onTap: () => getHistory(),
              ),
              SizedBox(height: 20),
              Text(
                'History',
                style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Color.fromRGBO(102, 102, 102, 1)),
              ),
              SizedBox(height: 100),
              InkWell(
                child: CircleAvatar(
                  backgroundColor: Colors.white,
                  backgroundImage: AssetImage("assets/icons/add.png"),
                  radius: 60,
                ),
                onTap: () async {
                  PermissionHandler().requestPermissions(
                      [PermissionGroup.camera]).then(_onStatusRequested);
                },
              ),
              SizedBox(height: 20),
              Text(
                'Tap to Capture Image',
                style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Color.fromRGBO(102, 102, 102, 1)),
              ),
              SizedBox(height: 100),
              InkWell(
                child: Image(image: AssetImage("assets/icons/gallery.png")),
                onTap: () async {
                  PermissionHandler().requestPermissions(
                      [PermissionGroup.mediaLibrary]).then(__onStatusRequested);
                },
              ),
              SizedBox(height: 20),
              Text(
                'Select from Gallery',
                style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Color.fromRGBO(102, 102, 102, 1)),
              )
            ],
          )
        ],
      ),
    );
  }

  void _onStatusRequested(Map<PermissionGroup, PermissionStatus> value) {
    final status = value[PermissionGroup.camera];
    if (status == PermissionStatus.granted) {
      imageSelectorCamera();
    } else {
      _updateStatus(status);
    }
  }

  void __onStatusRequested(Map<PermissionGroup, PermissionStatus> value) {
    final status = value[PermissionGroup.mediaLibrary];
    if (status == PermissionStatus.granted) {
      imageSelectorGallery();
    } else {
      _updateStatus(status);
    }
  }

  _updateStatus(PermissionStatus value) {
    if (value != _status) {
      setState(() {
        _status = value;
      });
    }
  }

  void imageSelectorCamera() async {
    var imageFile = await ImagePicker.pickImage(
      source: ImageSource.camera,
    );
    Future<bool> result = upload(imageFile);

    result
        .then((check) => Navigator.push(
              this.context,
              MaterialPageRoute(
                builder: (context) {
                  return ResultPage(
                      imageFile,
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
                },
              ),
            ))
        .catchError((e) => print(e));
  }

  void imageSelectorGallery() async {
    var imageFile = await ImagePicker.pickImage(
      source: ImageSource.gallery,
    );

    Future<bool> result = upload(imageFile);

    result
        .then((check) => Navigator.push(
              this.context,
              MaterialPageRoute(
                builder: (context) {
                  return ResultPage(
                      imageFile,
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
                },
              ),
            ))
        .catchError((e) => print(e));
  }

  Future<bool> upload(File imageFile) async {
    print(id);
    var request = http.MultipartRequest(
      'POST',
      Uri.parse("http://ec2-3-14-43-170.us-east-2.compute.amazonaws.com:5000/" +
          id +
          "/imageUpload"),
    );
    Map<String, String> headers = {"Content-type": "multipart/form-data"};
    request.files.add(
      http.MultipartFile(
        'image',
        imageFile.readAsBytes().asStream(),
        imageFile.lengthSync(),
        filename: imageFile.path,
        contentType: MediaType('jpg', 'jpeg'),
      ),
    );
    // print(imageFile)
    request.headers.addAll(headers);
    print("request: " + request.toString());
    print("image: " + imageFile.path);
    var response = await request.send();
    var responded = await http.Response.fromStream(response);
    responseData = json.decode(responded.body);
    recommended_foods = responseData["recommended_food_items"];
    print(recommended_foods);
    food = responseData["food"].toString();
    carbs = responseData["carbohydrates"].toString();
    calories = responseData["energy"].toString();
    cholestrol = responseData["cholesterol"].toString();
    fat = responseData["fat"].toString();
    fiber = responseData["fiber"].toString();
    protein = responseData["proteins"].toString();
    sugar = responseData["sugars"].toString();
    print(responseData);
    return true;
  }

  Future<bool> getHistory() async {
    print(id);
    final http.Response response = await http.get(
      'http://ec2-3-14-43-170.us-east-2.compute.amazonaws.com:5000/' +
          id +
          '/userHistory',
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
    );
    Map<String, dynamic> responseDatas = json.decode(response.body);
    List<dynamic> listUserHistory = responseDatas["user_history"];
    List<String> imageList = [];
    print(listUserHistory);
    for (int i = 0; i < listUserHistory.length; i++) {
      imageList.add(listUserHistory[i]["S3_Image_URI"]);
    }
    Navigator.push(
      this.context,
      MaterialPageRoute(
        builder: (context) {
          return GalleryPage(imageList, listUserHistory);
        },
      ),
    );
    print(imageList);
    return true;
  }
}
