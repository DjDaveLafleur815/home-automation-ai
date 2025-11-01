import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/trisensor.dart';

class ApiService {
  static const String baseUrl = "http://127.0.0.1:8000";

  static Future<List<TriSensor>> getTriSensors() async {
    final response = await http.get(Uri.parse("$baseUrl/trisensors"));

    if (response.statusCode == 200) {
      List<dynamic> data = jsonDecode(response.body)["trisensors"];
      return data.map((json) => TriSensor.fromJson(json)).toList();
    } else {
      throw Exception("Impossible de récupérer les capteurs");
    }
  }
}
