using System.Net.Http.Json;

namespace NeuroForge.Api.Services;

public sealed class MlInferenceClient(HttpClient httpClient)
{
    public async Task<MlPredictionResponse> PredictAsync(MlPredictionRequest request, CancellationToken cancellationToken)
    {
        var response = await httpClient.PostAsJsonAsync("predict", request, cancellationToken);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<MlPredictionResponse>(cancellationToken: cancellationToken)
            ?? throw new InvalidOperationException("ML service returned an empty response.");
    }
}
