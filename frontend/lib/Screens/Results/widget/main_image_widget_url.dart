import 'dart:io';

import 'package:flutter/material.dart';

class MainImageWidgetUrl extends StatelessWidget {
  String imageUrl;
  MainImageWidgetUrl(this.imageUrl);
  @override
  Widget build(BuildContext context) => Container(
          child: Center(
              child:
                  Row(mainAxisAlignment: MainAxisAlignment.center, children: [
        Image.network(imageUrl,
            width: MediaQuery.of(context).size.width * 0.5,
            height: MediaQuery.of(context).size.height * 0.5)
      ])));
}
