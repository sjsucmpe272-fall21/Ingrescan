import 'dart:io';

import 'package:flutter/material.dart';

class MainImageWidget extends StatelessWidget {
  File image;
  MainImageWidget(this.image);
  @override
  Widget build(BuildContext context) => Container(
          child: Center(
              child:
                  Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        SizedBox(height: 50),
        Image.file(image,
            width: MediaQuery.of(context).size.width * 0.5,
            height: MediaQuery.of(context).size.height * 0.5)
      ])));
}
