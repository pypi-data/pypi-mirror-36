/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips.
*/

__kernel void create_matrix(
    __global const float* vectors_x,
    __global const float* vectors_y,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const float e,
    const uint size,
    __global uint* matrix
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
            diff = vectors_x[(global_id_x * m) + i] - vectors_y[(global_id_y * m) + i];
            sum += diff * diff;
        }

        if (sum < e*e)
        {
            atomic_add(&matrix[(global_id_y / size) * dim_x + global_id_x], (convert_uint(1) << (global_id_y % size)));
        }
    }
}
