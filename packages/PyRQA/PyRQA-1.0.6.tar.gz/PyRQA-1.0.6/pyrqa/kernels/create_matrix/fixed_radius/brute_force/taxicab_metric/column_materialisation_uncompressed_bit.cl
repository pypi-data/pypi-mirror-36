/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips.
*/

__kernel void create_matrix(
    __global const float* time_series_x,
    __global const float* time_series_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const uint t,
    const float e,
    const uint size,
    __global uint* matrix
)
{
    uint global_id_x = get_global_id(0);
    uint global_id_y = get_global_id(1);

    if (global_id_x < dim_x)
    {
        float sum = 0.0f;

        for (uint i = 0; i < m; ++i)
        {
            sum += fabs(time_series_x[global_id_x + (i * t)] - time_series_y[global_id_y + (i * t)]);
        }

        if (sum < e)
        {
            atomic_add(&matrix[(global_id_y / size) * dim_x + global_id_x], (convert_uint(1) << (global_id_y % size)));
        }
    }
}
