# calculate forecast error
'''
 forecast_error = expected_error - predicted_value
  예측 오차              기대 오차
'''
expected =    [0.0, 0.5, 0.0, 0.5, 0.0]
predictions = [0.2, 0.4, 0.1, 0.6, 0.2]
forecast_errors = [expected[i]-predictions[i] for i in range(len(expected))]
print("Forecast Errors: %s" % forecast_errors)

bias = sum(forecast_errors) * 1.0 / len(expected)
print("Bias: %f"% bias)

