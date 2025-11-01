import 'package:flutter/material.dart';

class IAView extends StatelessWidget {
  const IAView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "IA / Ontologie",
          style: TextStyle(color: Colors.white),
        ),
      ),
      body: const Center(
        child: Text(
          "Écran IA (à connecter à Protégé & Neo4j)",
          style: TextStyle(color: Colors.white),
        ),
      ),
    );
  }
}
