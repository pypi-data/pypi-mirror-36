/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips.
*/

__kernel void create_uniform_grid(
    __global const float* time_series_y,
    __global const float* minimum,
    __global const uint* multiplicators,
    const uint dim_y,
    const uint m,
    const uint t,
    const float grid_edge_length,
    __global uint* grid_mapping
)
{
    uint id_y = get_global_id(0);

    if (id_y < dim_y)
    {
        uint grid_id = 0;
        for (uint i = 0; i < m; i++)
        {
            grid_id += convert_uint_rtz((time_series_y[id_y + (i * t)] - minimum[i]) / grid_edge_length) * multiplicators[i];
        }

        grid_mapping[id_y] = grid_id;
    }
}