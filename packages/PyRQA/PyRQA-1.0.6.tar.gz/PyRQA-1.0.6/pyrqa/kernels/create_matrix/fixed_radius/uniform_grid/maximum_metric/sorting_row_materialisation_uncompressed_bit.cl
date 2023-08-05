/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips.
*/

#ifdef cl_nv_pragma_unroll
   #pragma OPENCL EXTENSION cl_nv_pragma_unroll : enable
#endif

__kernel void create_matrix(
    __global const float* vectors_x,
    __global const float* vectors_y,
    __global float* minimum,
    __global uint* multiplicators,
    __global uint* grid_cells,
    __global uint* grid_cells_start,
    __global int* number_of_grid_cells,
    __global int* offset_coord,
    const uint dim_x,
    const uint m,
    const float e,
    const uint size,
    const float grid_edge_length,
    __global uint* matrix
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
            coordinate = convert_int_rtz((vectors_x[(id_x * m) + i] - minimum[i]) / grid_edge_length) - offset_coord[id_offset_coord * m + i];

            if (!(coordinate >= 0 && coordinate < number_of_grid_cells[i]))
            {
                return;
            }

            grid_id += convert_uint_rtz(coordinate) * multiplicators[i];
        }

        #pragma unroll loop_unroll
        for (uint i = grid_cells_start[grid_id]; i < grid_cells_start[grid_id + 1]; i++)
        {
            uint id_y = grid_cells[i];

            float max = 0.0f;

            for (uint j = 0; j < m; j++)
            {
                max = fmax(fabs(vectors_x[(id_x * m) + j] - vectors_y[(id_y * m) + j]), max);
            }

            if (max < e)
            {
                atomic_add(&matrix[(id_y / size) * dim_x + id_x], (convert_uint(1) << (id_y % size)));
            }
        }
    }
}

