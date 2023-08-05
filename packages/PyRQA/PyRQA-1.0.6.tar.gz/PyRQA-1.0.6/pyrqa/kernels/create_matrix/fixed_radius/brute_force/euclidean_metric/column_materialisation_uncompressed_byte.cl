/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips.
*/

__kernel void create_matrix(
    __global const float* time_series_x,
    __global const float* time_series_y,
    const uint dim_x,
    const uint m,
    const uint t,
    const float e,
    __global uchar* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        float diff;
        float sum = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            diff = time_series_x[global_id_x + (i * t)] - time_series_y[global_id_y + (i * t)];
            sum += diff * diff;
        }

        if (sum < e*e)
        {
            matrix[global_id_y * dim_x + global_id_x] = 1;
        }
        else
        {
            matrix[global_id_y * dim_x + global_id_x] = 0;
        }
    }
}
