import numpy as np

def calculate_psi(expected, actual, bucket_type='bins', buckets=10, axis=0):
    '''Calculate the PSI (Population Stability Index) for two distributions'''
    
    def psi(expected_array, actual_array, buckets):
        '''Calculate the PSI for a single variable
        Args:
           expected_array: numpy array of original values
           actual_array: numpy array of new values, same size as expected
           buckets: number of percentile ranges to make
        Returns:
           psi_value: calculated PSI value
        '''
        
        def scale_range (input, min, max):
            input += -(np.min(input))
            input /= np.max(input) / (max - min)
            input += min
            return input

        breakpoints = np.arange(0, buckets + 1) / (buckets) * 100

        if bucket_type == 'bins':
            breakpoints = np.histogram(expected_array, buckets)[1]
            # breakpoints = np.percentile(expected_array, breakpoints) # Not needed if using histogram directly

        expected_percents = np.histogram(expected_array, breakpoints)[0] / len(expected_array)
        actual_percents = np.histogram(actual_array, breakpoints)[0] / len(actual_array)

        # Handle zero buckets to avoid division by zero or log(0)
        expected_percents = np.where(expected_percents == 0, 0.0001, expected_percents)
        actual_percents = np.where(actual_percents == 0, 0.0001, actual_percents)

        psi_value = np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents))
        return psi_value

    # Simple mock implementation for MVP if not enough data
    # In a real system, you'd fetch the reference distribution from a training set
    # Here we just assume a reference normal distribution for demonstration
    if len(actual) < 2:
         return 0.0
         
    # Mock reference: Normal distribution
    expected_mock = np.random.normal(0.5, 0.1, 1000) 
    
    # Actually calculate against the mock reference for the demo
    return psi(expected_mock, np.array(actual), buckets)

def check_structure_shift(features):
    # Check for missing keys or type changes
    # Placeholder for MVP
    return 0.0
