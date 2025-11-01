import 'package:flutter/material.dart';
import '../models/trisensor.dart';
import '../services/api_service.dart';

class TriSensorView extends StatefulWidget {
  const TriSensorView({super.key});

  @override
  State<TriSensorView> createState() => _TriSensorViewState();
}

class _TriSensorViewState extends State<TriSensorView> {
  late Future<List<TriSensor>> futureTriSensors;

  @override
  void initState() {
    super.initState();
    futureTriSensors = ApiService.getTriSensors();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text("TriSensors", style: TextStyle(color: Colors.white)),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                futureTriSensors = ApiService.getTriSensors();
              });
            },
          ),
        ],
      ),
      body: FutureBuilder<List<TriSensor>>(
        future: futureTriSensors,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Text(
                "❌ Aucun TriSensor détecté",
                style: TextStyle(color: Colors.white, fontSize: 18),
              ),
            );
          }

          final sensors = snapshot.data!;

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: sensors.length,
            itemBuilder: (context, index) {
              final sensor = sensors[index];

              return Card(
                color: const Color(0xFF161B22),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(18),
                ),
                child: ListTile(
                  leading: const Icon(
                    Icons.sensors,
                    color: Colors.blueAccent,
                    size: 40,
                  ),
                  title: Text(
                    sensor.name,
                    style: const TextStyle(color: Colors.white),
                  ),
                  subtitle: Text(
                    sensor.id,
                    style: const TextStyle(color: Colors.white54),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
