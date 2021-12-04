import 'package:flutter/material.dart';
import 'package:flutter_auth/Screens/Login/login_screen.dart';
import 'package:flutter_auth/Screens/Results/page/result_page.dart';
import 'package:flutter_auth/Screens/Signup/components/background.dart';
import 'package:flutter_auth/components/already_have_an_account_acheck.dart';
import 'package:flutter_auth/components/rounded_button.dart';
import 'package:flutter_auth/components/rounded_input_field.dart';
import 'package:flutter_auth/components/rounded_password_field.dart';
import 'package:flutter_svg/svg.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Body extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    String fname = "";
    String lname = "";
    String mobile = "";
    String email = "";
    String password = "";
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
              "SIGNUP",
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: size.height * 0.03),
            SvgPicture.asset(
              "assets/icons/signup.svg",
              height: size.height * 0.35,
            ),
            RoundedInputField(
              hintText: "First Name",
              onChanged: (value) {
                fname = value;
              },
            ),
            RoundedInputField(
              hintText: "Last Name",
              onChanged: (value) {
                lname = value;
              },
            ),
            RoundedInputField(
              hintText: "Mobile Number",
              onChanged: (value) {
                mobile = value;
              },
            ),
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
              text: "SIGNUP",
              press: () {
                Future<bool> result =
                    signUp(fname, lname, mobile, email, password);
                bool check = true;
                result
                    .then((check) => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) {
                              return LoginScreen();
                            },
                          ),
                        ))
                    .catchError((e) => print(e));
              },
            ),
            SizedBox(height: size.height * 0.03),
            AlreadyHaveAnAccountCheck(
              login: false,
              press: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) {
                      return LoginScreen();
                    },
                  ),
                );
              },
            )
          ],
        ),
      ),
    ));
  }

  Future<bool> signUp(String fname, String lname, String mobile, String email,
      String password) async {
    final http.Response response = await http.post(
      'http://ec2-3-14-43-170.us-east-2.compute.amazonaws.com:5000/signup',
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        'fname': fname,
        'lname': lname,
        "phone": int.parse(mobile),
        "email": email,
        "password": password
      }),
    );
    print(jsonEncode(<String, dynamic>{
      'fname': fname,
      'lname': lname,
      "phone": int.parse(mobile),
      "email": email,
      "password": password
    }));
    print(response.body);
    if (response.statusCode == 200) {
      return true;
    } else {
      return false;
    }
  }
}
