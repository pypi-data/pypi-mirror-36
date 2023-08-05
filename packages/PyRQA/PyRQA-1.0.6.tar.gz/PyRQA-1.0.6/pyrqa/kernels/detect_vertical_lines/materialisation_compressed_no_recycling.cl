/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips
*/

#ifdef cl_nv_pragma_unroll
   #pragma OPENCL EXTENSION cl_nv_pragma_unroll : enable
#endif

__kernel void detect_vertical_lines(
    __global uint* indices,
    __global uint* indptr,
    const uint dim_x,
    const uint dim_y,
    const uint start_y,
    __global uint* recurrence_points,
    __global uint* vertical_frequency_distribution,
    __global uint* vertical_length_carryover,
    __global uint* vertical_index_carryover,
    __global uint* white_vertical_frequency_distribution,
    __global uchar* white_vertical_flag_carryover
)
{
    uint global_id_x = get_global_id(0);

    if (global_id_x < dim_x)
    {
        uint vertical_length = vertical_length_carryover[global_id_x];
        uint vertical_index = vertical_index_carryover[global_id_x];

        uint white_vertical_length;
        uint white_vertical_flag = white_vertical_flag_carryover[global_id_x];

        #pragma unroll loop_unroll
        for (uint id_y = indptr[global_id_x]; id_y < indptr[global_id_x + 1]; ++id_y)
        {
            uint global_id_y = start_y + indices[id_y];

            if (global_id_y - vertical_index == 1)
            {
                vertical_length++;
            }
            else
            {
                if (vertical_length > 0)
                {
                    atomic_inc(&vertical_frequency_distribution[vertical_length - 1]);
                }

                vertical_length = 1;
            }

            if (white_vertical_flag == 0)
            {
                white_vertical_length = global_id_y;
                white_vertical_flag = 1;
            }
            else
            {
                white_vertical_length = global_id_y - vertical_index - 1;
            }

            if(white_vertical_length > 0)
            {
                atomic_inc(&white_vertical_frequency_distribution[white_vertical_length - 1]);
            }

            vertical_index = global_id_y;
        }

        recurrence_points[global_id_x] += (indptr[global_id_x + 1] - indptr[global_id_x]);

        vertical_length_carryover[global_id_x] = vertical_length;
        vertical_index_carryover[global_id_x] = vertical_index;

        white_vertical_flag_carryover[global_id_x] = white_vertical_flag;
    }
}
