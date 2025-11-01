class TriSensor {
  final String id;
  final String name;
  final String type;

  TriSensor({required this.id, required this.name, required this.type});

  factory TriSensor.fromJson(Map<String, dynamic> json) {
    return TriSensor(id: json["id"], name: json["name"], type: json["type"]);
  }
}
