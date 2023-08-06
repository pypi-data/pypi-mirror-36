#include <torch/torch.h>
#include <vector>
#include <ATen/ATen.h>

at::Tensor padding(at::Tensor input, int pad_size ){// [left, right, up, down ]
    // This fuction only completes the function of zero-padding.
    auto size = input.sizes();
    auto padded = input.type().zeros({size[0]+2*pad_size, size[1]+2*pad_size});
    padded.type_as(input);
	for (int i = 0; i < size[0]; i++) {
		for (int j = 0; j < size[1]; j++) {
			padded[i+pad_size][j+pad_size] = input[i][j];
		}
	}
    return padded;
}


std::vector<at::Tensor> medidan_filter(at::Tensor input_patch,
                                       int filter_size, // now only for odd number
                                       int pad_size
                                       ){
    
    auto size = input_patch.sizes(); // size of  input and put put
    auto patch = input_patch.type().zeros({filter_size, filter_size});
    auto r = std::floor(filter_size/2);
    auto out_idx = input_patch.type().zeros({size[0], size[1],2});
    auto out_patch = input_patch.type().zeros({size[0], size[1]});
    // std::cout << "here1_in_median" << std::endl;
    auto padded_patch = padding(input_patch, pad_size);
	
    
    for(int i=0; i<size[0]; i++){
        for(int j=0; j<size[1]; j++){
            
            // extract patch
            for(int m=0; m<filter_size; m++)
            {
                for(int n=0; n<filter_size;n++){
                    patch[m][n] = padded_patch[i+m][j+n];
                }
            }
            
            //compute median and idx
            auto out = at::median(patch.reshape({1,filter_size * filter_size}), 1);
            
            auto value = std::get<0>(out)[0];
            //            std::cout<<value<<std::endl;
            out_patch[i][j] = value;
            //            std::cout<<out_patch<<std::endl;
            
            
            auto _x = std::get<1>(out) / filter_size;
            auto _y = std::get<1>(out) % filter_size;
            
            auto abs_x = i + _x - r;
            auto abs_y = j + _y - r;
            
            out_idx[i][j][0] = abs_x[0];
            out_idx[i][j][1] = abs_y[0];
        }
    }
    
    return {out_patch, out_idx};
}

std::vector<at::Tensor> median_filter_forward(
                                              at::Tensor input,
                                              int filter_size,
                                              int pad_size
                                              ){
    at::IntList input_tensor_size = input.sizes();
    auto output = input.type().zeros({input_tensor_size[0],input_tensor_size[1],input_tensor_size[2], input_tensor_size[3]});
    auto output_idx = input.type().zeros({input_tensor_size[0],input_tensor_size[1],input_tensor_size[2], input_tensor_size[3], 2});

    for(int n=0; n<input_tensor_size[0]; n++){
        for(int c=0; c<input_tensor_size[1]; c++){
            //do median filter and return result and idxs
            auto result = medidan_filter(input[n][c], filter_size, pad_size);
            output[n][c] = result[0];
            output_idx[n][c] = result[1];
        }
    }
    
    
    return {output, output_idx};
}


at::Tensor median_filter_backward(
                                  at::Tensor grad_h,
                                  at::Tensor median_idx){
    
    auto grad_input = grad_h * 0;
    
    auto size = grad_h.sizes();
    
    for(int n=0; n<size[0]; n++){
        for(int c=0; c<size[1]; c++){
            for(int x=0; x<size[2]; x++){
                for(int y=0; y<size[3]; y++){
                    //                    std::cout<<grad_h[n][c][x][y];
                    auto idx_x = median_idx[n][c][x][y][0].toCInt();
                    auto idx_y = median_idx[n][c][x][y][1].toCInt();
                    if(idx_x >=0 && idx_x < size[2] && idx_y >=0 && idx_y < size[3]){
                        //                        std::cout<<idx_x;
                        grad_input[n][c][idx_x][idx_y] += grad_h[n][c][x][y];
                    }
                    
                }
            }
        }
    }
    
    return grad_input;
}

 PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
   m.def("forward", &median_filter_forward, "MedianFilter forward");
   m.def("backward", &median_filter_backward, "MedianFilter backward");
 }
