import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:flutter_auth/Screens/Results/page/result_page.dart';
import 'package:path/path.dart';
import 'package:async/async.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'dart:convert';

class CameraPage extends StatefulWidget {
  @override
  _CameraPageState createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  List<CameraDescription> _cameras;
  CameraController _controller;
  bool _isReady = false;
  PermissionStatus _status;

  @override
  void initState() {
    super.initState();
    PermissionHandler()
        .checkPermissionStatus(PermissionGroup.camera)
        .then(_updateStatus);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.white, floatingActionButton: getFooter());
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
    upload(imageFile);

    Navigator.push(
      this.context,
      MaterialPageRoute(
        builder: (context) {
          return ResultPage();
        },
      ),
    );
  }

  void upload(File imageFile) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse(
          "http://ec2-3-14-43-170.us-east-2.compute.amazonaws.com:5000/f9ee5547-52a9-4421-8c0e-d0de3a6b0fd7/imageUpload"),
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
    final responseData = json.decode(responded.body);
    print(responseData);
  }

  void imageSelectorGallery() async {
    var imageFile = await ImagePicker.pickImage(
      source: ImageSource.gallery,
    );

    upload(imageFile);

    Navigator.push(
      this.context,
      MaterialPageRoute(
        builder: (context) {
          return ResultPage();
        },
      ),
    );
  }
}
