/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips.
*/

#ifdef cl_nv_pragma_unroll
   #pragma OPENCL EXTENSION cl_nv_pragma_unroll : enable
#endif

__kernel void create_matrix(
    __global const float* time_series_x,
    __global const float* time_series_y,
    __global float* minimum,
    __global uint* multiplicators,
    __global uint* grid_cells,
    __global uint* grid_counters,
    __global int* number_of_grid_cells,
    __global int* offset_coord,
    const uint dim_x,
    const uint dim_y,
    const uint m,
    const uint t,
    const float e,
    const float grid_edge_length,
    __global uchar* matrix
)
{
    uint id_x = get_global_id(0); // Index of the x vector
    uint id_offset_coord = get_global_id(1); // ID within offset_coord

    if (id_x < dim_x)
    {
        uint grid_id = 0;
        int coordinate;
        for (uint i = 0; i < m; i++)
        {
            coordinate = convert_int_rtz((time_series_x[id_x + (i * t)] - minimum[i]) / grid_edge_length) - offset_coord[id_offset_coord * m + i];

            if (!(coordinate >= 0 && coordinate < number_of_grid_cells[i]))
            {
                return;
            }

            grid_id += convert_uint_rtz(coordinate) * multiplicators[i];
        }

        #pragma unroll loop_unroll
        for (uint i = 0; i < grid_counters[grid_id]; i++)
        {
            uint id_y = grid_cells[grid_id * dim_y + i];

            float sum = 0.0f;

            for (uint j = 0; j < m; j++)
            {
                sum += fabs(time_series_x[id_x + (j * t)] - time_series_y[id_y + (j * t)]);
            }

            if (sum < e)
            {
                matrix[id_y * dim_x + id_x] = 1;
            }
        }
    }
}

