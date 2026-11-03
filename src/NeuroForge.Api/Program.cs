using Microsoft.SemanticKernel;
using NeuroForge.Api.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddHttpClient<MlInferenceClient>(client =>
{
    var baseUrl = builder.Configuration["ML_SERVICE_URL"] ?? "http://localhost:8000";
    client.BaseAddress = new Uri(baseUrl.TrimEnd('/') + "/");
    client.Timeout = TimeSpan.FromSeconds(15);
});
builder.Services.AddSingleton<AgentOrchestrator>();

var apiKey = builder.Configuration["OPENAI_API_KEY"];
var model = builder.Configuration["OPENAI_MODEL"] ?? "gpt-4o-mini";
if (!string.IsNullOrWhiteSpace(apiKey))
{
    builder.Services.AddSingleton(sp =>
    {
        var kernelBuilder = Kernel.CreateBuilder();
        kernelBuilder.AddOpenAIChatCompletion(model, apiKey);
        return kernelBuilder.Build();
    });
}
else
{
    builder.Services.AddSingleton(_ => Kernel.CreateBuilder().Build());
}

var app = builder.Build();

app.MapGet("/", () => Results.Ok(new
{
    name = "NeuroForge Agent Platform",
    version = "0.1.0",
    mode = string.IsNullOrWhiteSpace(apiKey) ? "deterministic-fallback" : "semantic-kernel-llm",
    endpoints = new[] { "/health", "/api/agent/ask", "/api/ml/predict" }
}));

app.MapGet("/health", () => Results.Ok(new { status = "healthy", service = "agent-api" }));

app.MapPost("/api/agent/ask", async (AgentRequest request, AgentOrchestrator agent, CancellationToken ct) =>
{
    if (string.IsNullOrWhiteSpace(request.Prompt))
        return Results.BadRequest(new { error = "Prompt is required." });

    var response = await agent.RunAsync(request.Prompt, ct);
    return Results.Ok(response);
});

app.MapPost("/api/ml/predict", async (MlPredictionRequest request, MlInferenceClient ml, CancellationToken ct) =>
{
    try
    {
        return Results.Ok(await ml.PredictAsync(request, ct));
    }
    catch (HttpRequestException ex)
    {
        return Results.Problem(title: "ML service unavailable", detail: ex.Message, statusCode: 503);
    }
});

app.Run();

public partial class Program { }
