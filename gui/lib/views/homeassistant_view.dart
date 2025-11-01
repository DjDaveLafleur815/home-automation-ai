import 'package:flutter/material.dart';

class HomeAssistantView extends StatelessWidget {
  const HomeAssistantView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "Home Assistant",
          style: TextStyle(color: Colors.white),
        ),
      ),
      body: const Center(
        child: Text(
          "Connexion Home Assistant OK ✅",
          style: TextStyle(color: Colors.white),
        ),
      ),
    );
  }
}
