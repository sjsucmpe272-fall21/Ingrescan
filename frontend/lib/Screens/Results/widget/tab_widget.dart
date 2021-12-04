import 'package:flutter/material.dart';

class TabWidget extends StatelessWidget {
  const TabWidget(
      {Key key, @required this.scrollController, @required this.responseData})
      : super(key: key);
  final ScrollController scrollController;
  final String responseData;

  @override
  Widget build(BuildContext context) => ListView(
        padding: EdgeInsets.all(16),
        controller: scrollController,
        children: [
          Text(responseData),
        ],
      );
}
