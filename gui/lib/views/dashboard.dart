import 'package:flutter/material.dart';
import 'trisensor_view.dart';
import 'ia_view.dart';
import 'homeassistant_view.dart';
import 'settings_view.dart';

class Dashboard extends StatelessWidget {
  const Dashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Smart Home Dashboard",
          style: TextStyle(color: Colors.white, fontSize: 20),
        ),
        backgroundColor: Colors.black,
      ),
      body: GridView.count(
        crossAxisCount: 2,
        padding: const EdgeInsets.all(16),
        children: [
          _dashboardCard(
            context,
            Icons.sensors,
            "Capteurs",
            const TriSensorView(),
          ),
          _dashboardCard(
            context,
            Icons.insights,
            "IA & Ontologie",
            const IAView(),
          ),
          _dashboardCard(
            context,
            Icons.home,
            "Home Assistant",
            const HomeAssistantView(),
          ),
          _dashboardCard(
            context,
            Icons.settings,
            "Configuration",
            const SettingsView(),
          ),
        ],
      ),
    );
  }

  Widget _dashboardCard(
    BuildContext context,
    IconData icon,
    String label,
    Widget page,
  ) {
    return Card(
      color: const Color(0xFF161B22),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: () =>
            Navigator.push(context, MaterialPageRoute(builder: (_) => page)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: Colors.blueAccent, size: 48),
            const SizedBox(height: 12),
            Text(label, style: const TextStyle(color: Colors.white)),
          ],
        ),
      ),
    );
  }
}
