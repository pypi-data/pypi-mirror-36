/*
This file is part of PyRQA.
Copyright 2015 Tobias Rawald, Mike Sips.
*/

__kernel void clear_buffer_uint8(
    __global uchar* buffer,
    const uchar value
)
{
    buffer[get_global_id(0)] = value;
}

__kernel void clear_buffer_uint32(
    __global uint* buffer,
    const uint value
)
{
    buffer[get_global_id(0)] = value;
}
