/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips
*/

__kernel void detect_diagonal_lines_symmetric(
    __global uint* indices,
    __global uint* indptr,
    const uint id_x,
    const uint dim_x,
    const uint start_x,
    const uint start_y,
    const uint w,
    const uint offset,
    __global uint* frequency_distribution,
    __global uint* length_carryover,
    __global uint* index_carryover
)
{
    uint thread_id = get_global_id(0);

    uint id_y = indices[indptr[id_x] + thread_id];

    uint global_id_x;
    uint global_id_y;

    uint carryover_id;

    uint length_buffer;

    if (id_x >= id_y + offset)
    {
        if (offset == 0)
        {
            carryover_id = id_x - id_y;
            global_id_x = start_x + id_x;
            global_id_y = start_y + id_y;
        }
        else
        {
            carryover_id = dim_x - id_x + id_y;
            global_id_x = start_y + id_y;
            global_id_y = start_x + id_x;
        }

        if (abs_diff(global_id_x, global_id_y) >= w)
        {
            length_buffer = length_carryover[carryover_id];

            if (global_id_y - index_carryover[carryover_id] == 1)
            {
                length_buffer++;
            }
            else
            {
                if (length_buffer > 0)
                {
                    atomic_inc(&frequency_distribution[length_buffer - 1]);
                }

                length_buffer = 1;
            }

            length_carryover[carryover_id] = length_buffer;
            index_carryover[carryover_id] = global_id_y;
        }
    }
}

