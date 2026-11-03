namespace NeuroForge.Api;

public sealed record AgentRequest(string Prompt);
public sealed record AgentResponse(string Answer, string Engine, DateTimeOffset Timestamp);
public sealed record MlPredictionRequest(Dictionary<string, double> Features);
public sealed record MlPredictionResponse(double Prediction, string ModelVersion, string Disclaimer);
