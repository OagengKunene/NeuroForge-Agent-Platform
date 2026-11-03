using System.Net;
using System.Net.Http.Json;
using Xunit;
using Microsoft.AspNetCore.Mvc.Testing;

namespace NeuroForge.Api.Tests;

public sealed class HealthTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public HealthTests(WebApplicationFactory<Program> factory) => _client = factory.CreateClient();

    [Fact]
    public async Task Health_ReturnsHealthy()
    {
        var response = await _client.GetAsync("/health");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
        Assert.Contains("healthy", await response.Content.ReadAsStringAsync());
    }

    [Fact]
    public async Task AgentEndpoint_RejectsEmptyPrompt()
    {
        var response = await _client.PostAsJsonAsync("/api/agent/ask", new { prompt = "" });
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
}
