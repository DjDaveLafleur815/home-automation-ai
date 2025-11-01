import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class TrisensorView extends StatefulWidget {
  const TrisensorView({super.key});

  @override
  State<TrisensorView> createState() => _TrisensorViewState();
}

class _TrisensorViewState extends State<TrisensorView> {
  List trisensors = [];
  bool loading = true;

  Future<void> fetchSensors() async {
    setState(() => loading = true);

    try {
      final response = await http.get(
        Uri.parse("http://192.168.1.22:8000/trisensors"),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() => trisensors = data["trisensors"]);
      }
    } catch (e) {
      debugPrint("Erreur TriSensor : $e");
    }

    setState(() => loading = false);
  }

  @override
  void initState() {
    super.initState();
    fetchSensors(); // <- on récupère les capteurs dès l'ouverture
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0D1117),
      appBar: AppBar(
        title: const Text("Capteurs TriSensor"),
        backgroundColor: Colors.black,
        actions: [
          IconButton(icon: const Icon(Icons.refresh), onPressed: fetchSensors),
        ],
      ),
      body: loading
          ? const Center(
              child: CircularProgressIndicator(color: Colors.blueAccent),
            )
          : trisensors.isEmpty
          ? const Center(
              child: Text(
                "Aucun capteur détecté",
                style: TextStyle(color: Colors.white70),
              ),
            )
          : GridView.builder(
              padding: const EdgeInsets.all(16),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
              ),
              itemCount: trisensors.length,
              itemBuilder: (context, index) {
                final sensor = trisensors[index];
                return _sensorCard(
                  title: sensor["name"],
                  value: sensor["value"].toString(),
                  unit: sensor["unit"] ?? "",
                );
              },
            ),
    );
  }

  Widget _sensorCard({
    required String title,
    required String value,
    required String unit,
  }) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(18),
        color: const Color(0xFF161B22),
        boxShadow: [
          BoxShadow(
            color: Colors.blueAccent.withOpacity(0.3),
            blurRadius: 8,
            spreadRadius: 1,
          ),
        ],
      ),
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Text(
            title,
            textAlign: TextAlign.center,
            style: const TextStyle(color: Colors.white, fontSize: 15),
          ),
          Text(
            "$value $unit",
            style: const TextStyle(
              color: Colors.blueAccent,
              fontSize: 26,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
