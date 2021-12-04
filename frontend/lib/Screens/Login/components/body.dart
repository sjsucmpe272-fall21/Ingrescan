import 'package:flutter/material.dart';
import 'package:flutter_auth/Screens/Login/components/background.dart';
import 'package:flutter_auth/Screens/Signup/signup_screen.dart';
import 'package:flutter_auth/Screens/Home/home_screen.dart';
import 'package:flutter_auth/components/already_have_an_account_acheck.dart';
import 'package:flutter_auth/components/rounded_button.dart';
import 'package:flutter_auth/components/rounded_input_field.dart';
import 'package:flutter_auth/components/rounded_password_field.dart';
import 'package:flutter_svg/svg.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

Map<String, dynamic> responseDatas;
var statusCode;

class Body extends StatelessWidget {
  const Body({
    Key key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    String email = "";
    String password = "";
    Size size = MediaQuery.of(context).size;
    return Background(
        child: Scaffold(
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
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            SizedBox(height: size.height * 0.03),
            Text(
              "LOGIN",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: size.height * 0.03),
            SvgPicture.asset(
              "assets/icons/login.svg",
              height: size.height * 0.35,
            ),
            SizedBox(height: size.height * 0.03),
            RoundedInputField(
              hintText: "Your Email",
              onChanged: (value) {
                email = value;
              },
            ),
            RoundedPasswordField(
              onChanged: (value) {
                password = value;
              },
            ),
            RoundedButton(
              text: "LOGIN",
              press: () {
                Future<bool> result = login(context, email, password);
              },
            ),
            SizedBox(height: size.height * 0.03),
            AlreadyHaveAnAccountCheck(
              press: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) {
                      return SignUpScreen();
                    },
                  ),
                );
              },
            ),
          ],
        ),
      ),
    ));
  }

  Future<bool> login(
      BuildContext context, String email, String password) async {
    String basicAuth = 'Basic ' + base64Encode(utf8.encode('$email:$password'));
    statusCode = 404;
    try {
      final http.Response response = await http.post(
        'http://ec2-3-14-43-170.us-east-2.compute.amazonaws.com:5000/login',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
          'authorization': basicAuth,
        },
      );
      responseDatas = json.decode(response.body);
      statusCode = response.statusCode;
    } catch (e) {
      print(e);
    } finally {
      print("HERE");

      if (statusCode == 200) {
        Navigator.push(context, MaterialPageRoute(
          builder: (context) {
            print(responseDatas["id"]);
            return CameraPage(responseDatas["id"]);
          },
        ));
      }
    }

    print(statusCode);
    return true;
  }
}
